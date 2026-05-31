from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# --- INICIO DE CÓDIGO AÑADIDO ---
from django.contrib.auth.decorators import login_required, user_passes_test # Para proteger vistas
from django.contrib.auth import login # Para iniciar sesión al registrarse
# --- FIN DE CÓDIGO AÑADIDO ---
from django.core.paginator import Paginator
from django.db.models import Q
from decouple import config
from .models import Producto, Categoria, Carrito, CarritoItem
# --- Importamos el nuevo formulario de registro ---
from .forms import ProductoForm, CategoriaForm, RegistroForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import re

# --- IMPORTACIONES NUEVAS PARA EL AGENTE DE IA EN AZURE ---
import os
from openai import AzureOpenAI

# Función auxiliar para verificar si el usuario es superusuario
def es_superusuario(user):
    return user.is_superuser

@login_required 
def lista_productos(request):
    productos_list = Producto.objects.filter(activo=True).select_related('categoria')
    
    # Búsqueda
    search_query = request.GET.get('search', '')
    if search_query:
        productos_list = productos_list.filter(
            Q(nombre__icontains=search_query) |
            Q(descripcion__icontains=search_query) |
            Q(codigo_barras__icontains=search_query)
        )
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos_list = productos_list.filter(categoria_id=categoria_id)
    
    estado_stock = request.GET.get('estado_stock')
    if estado_stock == 'bajo_stock':
        productos_list = [p for p in productos_list if p.estado_stock == 'bajo_stock']
    elif estado_stock == 'agotado':
        productos_list = productos_list.filter(stock=0)
    elif estado_stock == 'disponible':
        productos_list = [p for p in productos_list if p.estado_stock == 'disponible']
    
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    if precio_min:
        productos_list = productos_list.filter(precio__gte=precio_min)
    if precio_max:
        productos_list = productos_list.filter(precio__lte=precio_max)
    
    # Ordenamiento
    orden = request.GET.get('orden', '-fecha_creacion')
    if orden in ['nombre', '-nombre', 'precio', '-precio', 'stock', '-stock', 'fecha_creacion', '-fecha_creacion']:
        if isinstance(productos_list, list):
            # Si ya es una lista (por filtros de estado), convertir a queryset
            productos_ids = [p.id for p in productos_list]
            productos_list = Producto.objects.filter(id__in=productos_ids, activo=True).select_related('categoria')
        productos_list = productos_list.order_by(orden)
    
    # Paginación
    items_per_page = config('ITEMS_PER_PAGE', default=10, cast=int)
    paginator = Paginator(productos_list, items_per_page)
    
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    # Contexto adicional
    categorias = Categoria.objects.filter(activo=True)
    
    # Productos aleatorios para el carrusel (solo para usuarios no admin)
    productos_destacados = []
    if not request.user.is_superuser:
        # Obtener productos aleatorios con stock disponible
        productos_disponibles = Producto.objects.filter(activo=True, stock__gt=0).select_related('categoria')
        if productos_disponibles.count() >= 5:
            import random
            productos_destacados = random.sample(list(productos_disponibles), 5)
        else:
            productos_destacados = list(productos_disponibles)
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'search_query': search_query,
        'categoria_selected': categoria_id,
        'estado_stock_selected': estado_stock,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'orden_selected': orden,
        'total_productos': productos_list.count() if hasattr(productos_list, 'count') else len(productos_list),
        'productos_destacados': productos_destacados,
    }
    
    return render(request, 'productos/lista.html', context)

@login_required # <-- AÑADIDO: Proteger esta vista
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle.html', {'producto': producto})

@login_required
@user_passes_test(es_superusuario, login_url='lista_productos')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)  # Agregamos request.FILES para manejar archivos
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('producto_detalle', pk=producto.pk)
    else:
        form = ProductoForm()
    
    return render(request, 'productos/crear.html', {'form': form})

@login_required
@user_passes_test(es_superusuario, login_url='lista_productos')
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)  # Agregamos request.FILES
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('producto_detalle', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/editar.html', {'form': form, 'producto': producto})

@login_required
@user_passes_test(es_superusuario, login_url='lista_productos')
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.activo = False  # Eliminación lógica
        producto.save()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        return redirect('lista_productos')
    
    return render(request, 'productos/eliminar.html', {'producto': producto})

# Vistas para gestión de categorías
@login_required # <-- AÑADIDO: Proteger esta vista
def lista_categorias(request):
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    return render(request, 'productos/categorias/lista.html', {'categorias': categorias})

@login_required
@user_passes_test(es_superusuario, login_url='lista_productos')
def crear_categoria(request):
    from .forms import CategoriaForm
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    
    return render(request, 'productos/categorias/crear.html', {'form': form})

@login_required
@user_passes_test(es_superusuario, login_url='lista_productos')
def editar_categoria(request, pk):
    from .forms import CategoriaForm
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" actualizada exitosamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'productos/categorias/editar.html', {'form': form, 'categoria': categoria})

# Vistas para área de usuario y configuraciones
@login_required
def mi_perfil(request):
    """Vista para mostrar y editar el perfil del usuario"""
    return render(request, 'productos/usuario/perfil.html')

@login_required 
def configuracion(request):
    """Vista para configuraciones del sistema"""
    if request.method == 'POST':
        # Procesar configuraciones
        empresa_nombre = request.POST.get('empresa_nombre', 'TechStore Pro')
        items_por_pagina = request.POST.get('items_por_pagina', '12')
        tema = request.POST.get('tema', 'light')
        notificaciones = request.POST.get('notificaciones') == 'on'
        
        messages.success(request, 'Configuraciones guardadas exitosamente.')
        
    context = {
        'configuraciones': {
            'empresa_nombre': 'TechStore Pro',
            'items_por_pagina': 12,
            'tema': 'light',
            'notificaciones': True,
            'moneda': 'USD',
            'idioma': 'es',
            'zona_horaria': 'America/Mexico_City'
        }
    }
    return render(request, 'productos/usuario/configuracion.html', context)


def registrar_usuario(request):
    """Vista para registrar un nuevo usuario"""
    if request.user.is_authenticated:
        # Si el usuario ya está logueado, lo mandamos al inicio
        return redirect('lista_productos')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save() # Guarda el nuevo usuario en la base de datos
            login(request, user) # Inicia sesión automáticamente
            messages.success(request, f"¡Bienvenido, {user.username}! Tu cuenta ha sido creada.")
            return redirect('lista_productos')
    else:
        form = RegistroForm()
    
    return render(request, 'productos/registrar.html', {'form': form})


# --- VISTAS DEL CARRITO DE COMPRAS ---

@login_required
def ver_carrito(request):
    """Vista para mostrar el contenido del carrito"""
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.select_related('producto').all()
    
    context = {
        'carrito': carrito,
        'items': items,
        'total_items': carrito.total_items,
        'total_precio': carrito.total_precio,
    }
    return render(request, 'productos/carrito/ver.html', context)

@login_required
@require_POST
def agregar_al_carrito(request, producto_id):
    """Vista para agregar un producto al carrito"""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    cantidad = int(request.POST.get('cantidad', 1))
    
    # Verificar stock disponible
    if cantidad > producto.stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Solo hay {producto.stock} unidades disponibles'
            })
        messages.error(request, f'Solo hay {producto.stock} unidades disponibles de {producto.nombre}')
        return redirect('producto_detalle', pk=producto_id)
    
    # Obtener o crear carrito
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    # Verificar si el producto ya está en el carrito
    try:
        item = CarritoItem.objects.get(carrito=carrito, producto=producto)
        nueva_cantidad = item.cantidad + cantidad
        if nueva_cantidad > producto.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'No puedes agregar más. Solo hay {producto.stock} unidades disponibles'
                })
            messages.error(request, f'No puedes agregar más. Solo hay {producto.stock} unidades disponibles')
            return redirect('producto_detalle', pk=producto_id)
        item.cantidad = nueva_cantidad
        item.save()
    except CarritoItem.DoesNotExist:
        CarritoItem.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{producto.nombre} agregado al carrito',
            'total_items': carrito.total_items
        })
    
    messages.success(request, f'{producto.nombre} agregado al carrito')
    return redirect('producto_detalle', pk=producto_id)

@login_required
@require_POST
def actualizar_carrito(request, item_id):
    """Vista para actualizar la cantidad de un item en el carrito"""
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    nueva_cantidad = int(request.POST.get('cantidad', 1))
    
    if nueva_cantidad > item.producto.stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Solo hay {item.producto.stock} unidades disponibles'
            })
        messages.error(request, f'Solo hay {item.producto.stock} unidades disponibles')
        return redirect('ver_carrito')
    
    if nueva_cantidad <= 0:
        item.delete()
        message = f'{item.producto.nombre} eliminado del carrito'
    else:
        item.cantidad = nueva_cantidad
        item.save()
        message = f'Cantidad actualizada para {item.producto.nombre}'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        carrito = item.carrito if nueva_cantidad > 0 else Carrito.objects.get(usuario=request.user)
        return JsonResponse({
            'success': True,
            'message': message,
            'total_items': carrito.total_items,
            'total_precio': float(carrito.total_precio),
            'item_subtotal': float(item.subtotal) if nueva_cantidad > 0 else 0
        })
    
    messages.success(request, message)
    return redirect('ver_carrito')

@login_required
@require_POST
def remover_del_carrito(request, item_id):
    """Vista para remover un item del carrito"""
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    producto_nombre = item.producto.nombre
    item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        carrito = Carrito.objects.get(usuario=request.user)
        return JsonResponse({
            'success': True,
            'message': f'{producto_nombre} eliminado del carrito',
            'total_items': carrito.total_items,
            'total_precio': float(carrito.total_precio)
        })
    
    messages.success(request, f'{producto_nombre} eliminado del carrito')
    return redirect('ver_carrito')

@login_required
@require_POST
def limpiar_carrito(request):
    """Vista para limpiar todo el carrito"""
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        carrito.limpiar()
        messages.success(request, 'Carrito limpiado exitosamente')
    except Carrito.DoesNotExist:
        messages.remove(request, 'El carrito ya está vacío')
    
    return redirect('ver_carrito')

@login_required
def procesar_compra(request):
    """Vista para procesar la compra (checkout)"""
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items = carrito.items.select_related('producto').all()
        
        if not items:
            messages.warning(request, 'Tu carrito está vacío')
            return redirect('lista_productos')
        
        # Verificar stock antes de procesar
        for item in items:
            if item.cantidad > item.producto.stock:
                messages.error(request, f'No hay suficiente stock para {item.producto.nombre}')
                return redirect('ver_carrito')
        
        if request.method == 'POST':
            # Reducir stock
            for item in items:
                producto = item.producto
                producto.stock -= item.cantidad
                producto.save()
            
            # Limpiar carrito
            carrito.limpiar()
            
            messages.success(request, '¡Compra realizada exitosamente!')
            return redirect('lista_productos')
        
        context = {
            'carrito': carrito,
            'items': items,
            'total_precio': carrito.total_precio,
        }
        return render(request, 'productos/carrito/checkout.html', context)
        
    except Carrito.DoesNotExist:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('lista_productos')



@login_required
@require_POST
def agregar_al_carrito_agente(request):
    """
    Endpoint para que el agente de IA agregue productos al carrito.
    Recibe JSON con 'producto_id' y 'cantidad'
    """
    try:
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = int(data.get('cantidad', 1))
        
        if not producto_id:
            return JsonResponse({
                'success': False,
                'message': 'ID del producto requerido'
            }, status=400)
        
        # Validar que la cantidad sea positiva
        if cantidad <= 0:
            return JsonResponse({
                'success': False,
                'message': 'La cantidad debe ser mayor a 0'
            }, status=400)
        
        # Obtener el producto
        producto = get_object_or_404(Producto, id=producto_id, activo=True)
        
        # Verificar stock disponible
        if cantidad > producto.stock:
            return JsonResponse({
                'success': False,
                'message': f'Solo hay {producto.stock} unidades disponibles de {producto.nombre}'
            }, status=400)
        
        # Obtener o crear carrito
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        
        # Agregar producto al carrito
        try:
            item = CarritoItem.objects.get(carrito=carrito, producto=producto)
            nueva_cantidad = item.cantidad + cantidad
            if nueva_cantidad > producto.stock:
                return JsonResponse({
                    'success': False,
                    'message': f'No puedes agregar más. Solo hay {producto.stock} unidades disponibles'
                }, status=400)
            item.cantidad = nueva_cantidad
            item.save()
        except CarritoItem.DoesNotExist:
            CarritoItem.objects.create(carrito=carrito, producto=producto, cantidad=cantidad)
        
        return JsonResponse({
            'success': True,
            'message': f'✓ {cantidad} x {producto.nombre} agregado(s) al carrito',
            'total_items': carrito.total_items,
            'total_precio': float(carrito.total_precio),
            'producto_nombre': producto.nombre,
            'cantidad': cantidad
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Formato JSON inválido'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al agregar producto: {str(e)}'
        })


@login_required
@require_POST
def remover_del_carrito_agente(request):
    """
    Endpoint para que el agente de IA elimine productos del carrito.
    Recibe JSON con 'producto_id'
    """
    try:
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        
        if not producto_id:
            return JsonResponse({
                'success': False,
                'message': 'ID del producto requerido'
            })
        
        # Obtener el carrito del usuario
        carrito = Carrito.objects.get(usuario=request.user)
        
        # Eliminar el producto del carrito
        item = CarritoItem.objects.get(carrito=carrito, producto_id=producto_id)
        producto_nombre = item.producto.nombre
        item.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'✓ {producto_nombre} eliminado del carrito',
            'total_items': carrito.total_items,
            'total_precio': float(carrito.total_precio)
        })
        
    except Carrito.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'No tienes un carrito activo'
        })
    except CarritoItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Este producto no está en tu carrito'
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Formato JSON inválido'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al eliminar producto: {str(e)}'
        })


@login_required
@require_POST
def actualizar_cantidad_carrito_agente(request):
    """
    Endpoint para que el agente de IA modifique la cantidad de un producto en el carrito.
    Recibe JSON con 'producto_id' y 'cantidad'
    """
    try:
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        nueva_cantidad = int(data.get('cantidad', 1))
        
        if not producto_id:
            return JsonResponse({
                'success': False,
                'message': 'ID del producto requerido'
            })
        
        if nueva_cantidad <= 0:
            return JsonResponse({
                'success': False,
                'message': 'La cantidad debe ser mayor a 0'
            })
        
        # Obtener el carrito del usuario
        carrito = Carrito.objects.get(usuario=request.user)
        
        # Obtener el item del carrito
        item = CarritoItem.objects.get(carrito=carrito, producto_id=producto_id)
        producto = item.producto
        
        # Validar stock disponible
        if nueva_cantidad > producto.stock:
            return JsonResponse({
                'success': False,
                'message': f'Solo hay {producto.stock} unidades disponibles de {producto.nombre}'
            })
        
        # Actualizar cantidad
        item.cantidad = nueva_cantidad
        item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'✓ Cantidad de {producto.nombre} actualizada a {nueva_cantidad}',
            'total_items': carrito.total_items,
            'total_precio': float(carrito.total_precio),
            'item_cantidad': nueva_cantidad,
            'item_subtotal': float(item.subtotal)
        })
        
    except Carrito.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'No tienes un carrito activo'
        })
    except CarritoItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Este producto no está en tu carrito'
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Formato JSON inválido'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al actualizar cantidad: {str(e)}'
        })


@login_required
def responder_chatbot(request):
    """Vista asíncrona que gestiona la comunicación con el Agente de Azure OpenAI"""
    if request.method == "POST":
        mensaje_usuario = request.POST.get("mensaje", "")
        
        if not mensaje_usuario:
            return JsonResponse({"success": False, "message": "El mensaje no puede estar vacío."})
        
        try:
            # Obtenemos el inventario dinámico de la base de datos relacional
            inventario = Producto.objects.filter(activo=True).select_related('categoria')

            # Estructurar el catálogo incluyendo el ID del producto para el mapeo de URLs
            lineas_catalogo = []
            for prod in inventario:
                # Verificamos si tiene categoría antes de sacar su nombre
                nombre_categoria = prod.categoria.nombre if prod.categoria else "Sin categoría"
                
                lineas_catalogo.append(
                    f"- ID: {prod.id} | {prod.nombre} | Categoría: {nombre_categoria} | Precio: ${prod.precio} | Stock: {prod.stock} unidades."
                )
            contexto_productos = "\n".join(lineas_catalogo)
                        
            #  Inicializamos el cliente oficial SDK de Azure 
            client = AzureOpenAI(
                azure_endpoint=config("AZURE_OPENAI_ENDPOINT"),
                api_key=config("AZURE_OPENAI_KEY"),
                api_version="2024-02-15-preview"
            )
            
            # Definir el System Prompt del asistente mejorado
            system_prompt = (
                "Eres 'TechBot', el asistente virtual inteligente del supermercado tecnológico TechStore Pro. "
                "Tu objetivo es ayudar amablemente a los usuarios basándote ÚNICAMENTE en el inventario real provisto.\n\n"
                "Lista oficial del inventario en tiempo real:\n"
                f"{contexto_productos}\n\n"
                "Directrices obligatorias:\n"
                "1. Sé sumamente educado y servicial.\n"
                "2. REGLA DE REDIRECCIÓN CRÍTICA: Cada vez que menciones un producto que SÍ está disponible en el catálogo, "
                "debes incluir OBLIGATORIAMENTE su ID al lado de su nombre usando el formato estricto: [LINK:ID]. "
                "Por ejemplo, si el producto 'Laptop HP' tiene ID 5, debes escribirlo exactamente como: Laptop HP [LINK:5]. "
                "No inventes IDs, usa solo los provistos en la lista.\n"
                "3. Si un producto de la lista tiene stock = 0, aclara que está agotado actualmente.\n"
                "4. ¡No alucines ni inventes precios o características!\n\n"
                "FUNCIONALIDAD DE CARRITO DE COMPRAS:\n"
                "El usuario puede gestionar su carrito de varias formas:\n\n"
                "A) AGREGAR PRODUCTOS:\n"
                "Si el usuario dice que quiere agregar un producto (ej: 'agrega zapatillas', 'guarda este producto', 'compra 2 zapatos'), debes:\n"
                "- Identificar qué producto quiere agregar\n"
                "- Extraer la cantidad (si no especifica, asume 1)\n"
                "- Incluir este botón: [AGREGAR_AL_CARRITO:ID_PRODUCTO:CANTIDAD]\n"
                "Ejemplo: 'Te agregaré 2 Zapatillas Nike al carrito. [AGREGAR_AL_CARRITO:7:2]'\n\n"
                "B) ELIMINAR PRODUCTOS:\n"
                "Si el usuario dice que quiere eliminar un producto (ej: 'elimina las zapatillas', 'saca esto del carrito', 'quítame los iPhones'), debes:\n"
                "- Identificar qué producto quiere eliminar\n"
                "- Incluir este botón: [ELIMINAR_DEL_CARRITO:ID_PRODUCTO]\n"
                "Ejemplo: 'Eliminaré las Zapatillas Nike de tu carrito. [ELIMINAR_DEL_CARRITO:7]'\n\n"
                "C) MODIFICAR CANTIDAD:\n"
                "Si el usuario dice que quiere cambiar la cantidad (ej: 'cambiar a 3', 'modifica la cantidad a 5', 'quiero solo 1'), debes:\n"
                "- Identificar qué producto\n"
                "- Extraer la nueva cantidad\n"
                "- Incluir este botón: [ACTUALIZAR_CANTIDAD_CARRITO:ID_PRODUCTO:NUEVA_CANTIDAD]\n"
                "Ejemplo: 'Cambiaré la cantidad de iPhones a 3. [ACTUALIZAR_CANTIDAD_CARRITO:5:3]'\n\n"
                "IMPORTANTE:\n"
                "- Si el producto no existe, avisa al usuario\n"
                "- Si no hay suficiente stock, informa la disponibilidad\n"
                "- Siempre confirma la acción con el botón correspondiente"
            )
                        
            #  Enviar la petición al modelo 
            response = client.chat.completions.create(
                model=config("AZURE_OPENAI_DEPLOYMENT_NAME", default="gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": mensaje_usuario}
                ],
                temperature=0.7
            )
            
            # Extraer los resultados
            respuesta_ia = response.choices[0].message.content
            
            # Procesar los botones de acción [AGREGAR_AL_CARRITO:ID:CANTIDAD]
            respuesta_procesada = _procesar_acciones_agente(respuesta_ia, request.user)
            
            return JsonResponse({"success": True, "respuesta": respuesta_procesada})
            
        except Exception as e:
            
            print(f"ERROR CRÍTICO DE AZURE: {str(e)}") 
            
            return JsonResponse({"success": False, "message": f"Error en el servicio de IA: {str(e)}"})
            
    return JsonResponse({"success": False, "message": "Método HTTP no válido."})


def _procesar_acciones_agente(respuesta, usuario):
    """
    Procesa las acciones del agente:
    - [AGREGAR_AL_CARRITO:ID:CANTIDAD]
    - [ELIMINAR_DEL_CARRITO:ID]
    - [ACTUALIZAR_CANTIDAD_CARRITO:ID:CANTIDAD]
    Las reemplaza con botones interactivos
    """
    
    # Patrón para encontrar [AGREGAR_AL_CARRITO:ID:CANTIDAD]
    patron_agregar = r'\[AGREGAR_AL_CARRITO:(\d+):(\d+)\]'
    def reemplazar_agregar(match):
        producto_id = match.group(1)
        cantidad = match.group(2)
        return f"<button class='btn btn-sm btn-success mt-1 btn-agregar-carrito-agente d-inline-block' data-producto-id='{producto_id}' data-cantidad='{cantidad}' style='font-size: 11px; padding: 2px 8px;'>✓ Agregar al Carrito</button>"
    
    # Patrón para encontrar [ELIMINAR_DEL_CARRITO:ID]
    patron_eliminar = r'\[ELIMINAR_DEL_CARRITO:(\d+)\]'
    def reemplazar_eliminar(match):
        producto_id = match.group(1)
        return f"<button class='btn btn-sm btn-danger mt-1 btn-eliminar-carrito-agente d-inline-block' data-producto-id='{producto_id}' style='font-size: 11px; padding: 2px 8px;'>✗ Eliminar del Carrito</button>"
    
    # Patrón para encontrar [ACTUALIZAR_CANTIDAD_CARRITO:ID:CANTIDAD]
    patron_actualizar = r'\[ACTUALIZAR_CANTIDAD_CARRITO:(\d+):(\d+)\]'
    def reemplazar_actualizar(match):
        producto_id = match.group(1)
        cantidad = match.group(2)
        return f"<button class='btn btn-sm btn-warning mt-1 btn-actualizar-cantidad-agente d-inline-block' data-producto-id='{producto_id}' data-cantidad='{cantidad}' style='font-size: 11px; padding: 2px 8px;'>⟷ Actualizar Cantidad</button>"
    
    # Aplicar reemplazos
    respuesta = re.sub(patron_agregar, reemplazar_agregar, respuesta)
    respuesta = re.sub(patron_eliminar, reemplazar_eliminar, respuesta)
    respuesta = re.sub(patron_actualizar, reemplazar_actualizar, respuesta)
    
    return respuesta