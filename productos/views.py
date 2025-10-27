from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# --- INICIO DE CÓDIGO AÑADIDO ---
from django.contrib.auth.decorators import login_required # Para proteger vistas
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

@login_required # <-- AÑADIDO: Proteger esta vista
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
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'search_query': search_query,
        'categoria_selected': categoria_id,
        'estado_stock_selected': estado_stock,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'orden_selected': orden,
        'total_productos': productos_list.count() if hasattr(productos_list, 'count') else len(productos_list)
    }
    
    return render(request, 'productos/lista.html', context)

@login_required # <-- AÑADIDO: Proteger esta vista
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle.html', {'producto': producto})

@login_required # <-- AÑADIDO: Proteger esta vista
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('producto_detalle', pk=producto.pk)
    else:
        form = ProductoForm()
    
    return render(request, 'productos/crear.html', {'form': form})

@login_required # <-- AÑADIDO: Proteger esta vista
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('producto_detalle', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/editar.html', {'form': form, 'producto': producto})

@login_required # <-- AÑADIDO: Proteger esta vista
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

@login_required # <-- AÑADIDO: Proteger esta vista
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

@login_required # <-- AÑADIDO: Proteger esta vista
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
@login_required # <-- AÑADIDO: Proteger esta vista
def mi_perfil(request):
    """Vista para mostrar y editar el perfil del usuario"""
    # --- MODIFICADO ---
    # Ya no se necesita el contexto falso. El objeto 'user'
    # (request.user) está disponible automáticamente en la plantilla.
    return render(request, 'productos/usuario/perfil.html')

@login_required # <-- AÑADIDO: Proteger esta vista
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

# --- ELIMINADO ---
# La función 'cerrar_sesion' se elimina porque Django la manejará
# automáticamente a través de la URL de 'logout'.


# --- INICIO DE CÓDIGO NUEVO AÑADIDO ---

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
    
    # Muestra la plantilla con el formulario (vacío o con errores)
    return render(request, 'productos/registrar.html', {'form': form})

# --- FIN DE CÓDIGO NUEVO AÑADIDO ---


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
        messages.info(request, 'El carrito ya está vacío')
    
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
            # Aquí procesarías el pago real
            # Por ahora solo simularemos la compra
            
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