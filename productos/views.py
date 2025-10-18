from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Producto
from .forms import ProductoForm

def lista_productos(request):
    productos_list = Producto.objects.filter(activo=True)
    paginator = Paginator(productos_list, 10)  # 10 productos por página
    
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    return render(request, 'productos/lista.html', {'productos': productos})

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