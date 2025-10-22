from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from decouple import config
from .models import Producto, Categoria
from .forms import ProductoForm

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

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle.html', {'producto': producto})

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
def lista_categorias(request):
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    return render(request, 'productos/categorias/lista.html', {'categorias': categorias})

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
def mi_perfil(request):
    """Vista para mostrar y editar el perfil del usuario"""
    context = {
        'usuario': {
            'nombre': 'Administrador',
            'email': 'admin@techstore.com',
            'rol': 'Administrador del Sistema',
            'fecha_registro': '2024-01-15',
            'ultimo_acceso': '2024-10-21 14:30',
            'productos_creados': 13,
            'categorias_creadas': 8
        }
    }
    return render(request, 'productos/usuario/perfil.html', context)

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

def cerrar_sesion(request):
    """Vista para cerrar sesión"""
    messages.info(request, 'Sesión cerrada exitosamente.')
    return redirect('lista_productos')