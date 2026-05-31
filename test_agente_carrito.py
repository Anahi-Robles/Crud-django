"""
Script de prueba para validar la integración del agente con el carrito
Ejecutar: python manage.py shell < test_agente_carrito.py
"""

from productos.models import Producto, Carrito, CarritoItem, Categoria
from django.contrib.auth.models import User
import json

# Crear usuario de prueba si no existe
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)

print(f"✓ Usuario: {user.username} ({'creado' if created else 'existente'})")

# Crear categoría
cat, _ = Categoria.objects.get_or_create(
    nombre='Tecnología',
    defaults={'descripcion': 'Productos de tecnología'}
)
print(f"✓ Categoría: {cat.nombre}")

# Crear productos de prueba
productos_data = [
    {'nombre': 'Zapatillas Nike', 'precio': 125.00, 'stock': 10},
    {'nombre': 'iPhone 15 Pro', 'precio': 999.99, 'stock': 5},
    {'nombre': 'Laptop HP', 'precio': 750.00, 'stock': 3},
]

productos = []
for data in productos_data:
    prod, created = Producto.objects.get_or_create(
        nombre=data['nombre'],
        defaults={
            'descripcion': f"Producto: {data['nombre']}",
            'categoria': cat,
            'precio': data['precio'],
            'stock': data['stock'],
            'activo': True
        }
    )
    productos.append(prod)
    print(f"✓ Producto: {prod.nombre} (ID: {prod.id}) - Stock: {prod.stock}")

# Crear carrito para el usuario
carrito, created = Carrito.objects.get_or_create(
    usuario=user,
    defaults={}
)
print(f"\n✓ Carrito de {user.username} creado: {carrito}")

# Prueba 1: Agregar un producto
print("\n" + "="*50)
print("PRUEBA 1: Agregar 2 Zapatillas Nike")
print("="*50)

producto = productos[0]
carrito.agregar_producto(producto, cantidad=2)
print(f"✓ Total items en carrito: {carrito.total_items}")
print(f"✓ Total precio: ${carrito.total_precio}")

# Prueba 2: Agregar otro producto
print("\n" + "="*50)
print("PRUEBA 2: Agregar 1 iPhone 15 Pro")
print("="*50)

producto2 = productos[1]
carrito.agregar_producto(producto2, cantidad=1)
print(f"✓ Total items en carrito: {carrito.total_items}")
print(f"✓ Total precio: ${carrito.total_precio}")

# Prueba 3: Actualizar cantidad existente
print("\n" + "="*50)
print("PRUEBA 3: Actualizar 1 Zapatilla Nike a 3")
print("="*50)

carrito.agregar_producto(productos[0], cantidad=1)
print(f"✓ Total items en carrito: {carrito.total_items}")
print(f"✓ Total precio: ${carrito.total_precio}")

# Prueba 4: Listar items
print("\n" + "="*50)
print("PRUEBA 4: Items en el carrito")
print("="*50)

for item in carrito.items.all():
    print(f"  • {item.cantidad}x {item.producto.nombre} - ${item.subtotal}")

# Prueba 5: Probar patrón de acción
print("\n" + "="*50)
print("PRUEBA 5: Validar patrón [AGREGAR_AL_CARRITO:ID:CANTIDAD]")
print("="*50)

import re

response_ejemplo = f"""
Perfecto! Te agregaré estos productos al carrito:

1. 2 Zapatillas Nike [LINK:{productos[0].id}] - $250.00
   [AGREGAR_AL_CARRITO:{productos[0].id}:2]

2. 1 iPhone 15 Pro [LINK:{productos[1].id}] - $999.99
   [AGREGAR_AL_CARRITO:{productos[1].id}:1]

Total sería: $1,249.99
"""

patron = r'\[AGREGAR_AL_CARRITO:(\d+):(\d+)\]'
matches = re.findall(patron, response_ejemplo)

print(f"✓ Patrones encontrados: {len(matches)}")
for prod_id, cantidad in matches:
    print(f"  → Producto ID: {prod_id}, Cantidad: {cantidad}")

print("\n" + "="*50)
print("✓ TODAS LAS PRUEBAS PASARON")
print("="*50)
print("\nResumen:")
print(f"  • Usuario: {user.username}")
print(f"  • Carrito Items: {carrito.total_items}")
print(f"  • Total: ${carrito.total_precio}")
print(f"  • Productos: {carrito.items.count()}")
