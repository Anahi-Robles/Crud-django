from .models import Carrito

def carrito_context(request):
    """Context processor para mostrar información del carrito en todas las plantillas"""
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            total_items = carrito.total_items
        except Carrito.DoesNotExist:
            total_items = 0
    else:
        total_items = 0
    
    return {
        'carrito_total_items': total_items
    }