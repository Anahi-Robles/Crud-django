from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# --- INICIO DE CÓDIGO AÑADIDO ---
from django.contrib.auth.decorators import login_required # Para proteger vistas
from django.contrib.auth import login # Para iniciar sesión al registrarse
# --- FIN DE CÓDIGO AÑADIDO ---
from django.core.paginator import Paginator
from django.db.models import Q
from decouple import config
from .models import Producto, Categoria
# --- Importamos el nuevo formulario de registro ---
from .forms import ProductoForm, CategoriaForm, RegistroForm

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