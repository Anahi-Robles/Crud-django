from django.urls import path
# Importa las vistas de autenticación de Django
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Productos
    path('', views.lista_productos, name='lista_productos'),
    path('producto/<int:pk>/', views.detalle_producto, name='producto_detalle'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('producto/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('producto/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    
    # Categorías
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    
    # --- Autenticación ---
    
    # Login
    path('login/', auth_views.LoginView.as_view(
        template_name='productos/login.html',
        redirect_authenticated_user=True 
    ), name='login'),
    
    # Registro
    path('registrar/', views.registrar_usuario, name='registrar'),
    
    # Logout
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Vistas de Usuario
    path('mi-perfil/', views.mi_perfil, name='mi_perfil'),
    path('configuracion/', views.configuracion, name='configuracion'),
]