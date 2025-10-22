from django.core.management.base import BaseCommand
from productos.models import Categoria, Producto
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea categorías y productos de ejemplo para la aplicación'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando categorías y productos de ejemplo...'))
        
        # Crear categorías
        categorias_data = [
            {
                'nombre': 'Electrónicos',
                'descripcion': 'Dispositivos electrónicos, gadgets y accesorios tecnológicos'
            },
            {
                'nombre': 'Ropa y Accesorios',
                'descripcion': 'Prendas de vestir, calzado y accesorios de moda'
            },
            {
                'nombre': 'Hogar y Jardín',
                'descripcion': 'Artículos para el hogar, decoración y jardinería'
            },
            {
                'nombre': 'Deportes y Fitness',
                'descripcion': 'Equipamiento deportivo, ropa deportiva y suplementos'
            },
            {
                'nombre': 'Libros y Medios',
                'descripcion': 'Libros, revistas, música y contenido multimedia'
            },
            {
                'nombre': 'Salud y Belleza',
                'descripcion': 'Productos de cuidado personal, cosméticos y salud'
            },
            {
                'nombre': 'Automóviles',
                'descripcion': 'Repuestos, accesorios y productos para vehículos'
            },
            {
                'nombre': 'Juguetes y Juegos',
                'descripcion': 'Juguetes para niños, juegos de mesa y entretenimiento'
            }
        ]
        
        categorias_creadas = []
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            if created:
                categorias_creadas.append(categoria)
                self.stdout.write(f'✓ Categoría creada: {categoria.nombre}')
            else:
                self.stdout.write(f'- Categoría ya existe: {categoria.nombre}')
        
        # Crear productos de ejemplo
        productos_data = [
            # Electrónicos
            {
                'nombre': 'iPhone 15 Pro',
                'descripcion': 'Smartphone Apple iPhone 15 Pro con chip A17 Pro, cámara de 48MP y pantalla Super Retina XDR de 6.1 pulgadas.',
                'categoria': 'Electrónicos',
                'precio': Decimal('999.99'),
                'stock': 25,
                'stock_minimo': 5,
                'codigo_barras': 'APL-IP15P-128',
                'imagen': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop&crop=center'
            },
            {
                'nombre': 'Samsung Galaxy S24',
                'descripcion': 'Smartphone Samsung Galaxy S24 con procesador Snapdragon 8 Gen 3, cámara de 50MP y pantalla Dynamic AMOLED de 6.2 pulgadas.',
                'categoria': 'Electrónicos',
                'precio': Decimal('849.99'),
                'stock': 18,
                'stock_minimo': 5,
                'codigo_barras': 'SAM-GS24-256',
                'imagen': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&crop=center'
            },
            {
                'nombre': 'MacBook Air M3',
                'descripcion': 'Laptop Apple MacBook Air con chip M3, pantalla Liquid Retina de 13.6 pulgadas, 8GB RAM y 256GB SSD.',
                'categoria': 'Electrónicos',
                'precio': Decimal('1199.99'),
                'stock': 12,
                'stock_minimo': 3,
                'codigo_barras': 'APL-MBA-M3-256',
                'imagen': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop&crop=center'
            },
            
            # Ropa y Accesorios
            {
                'nombre': 'Camiseta Nike Dri-FIT',
                'descripcion': 'Camiseta deportiva Nike con tecnología Dri-FIT para mantener la piel seca y cómoda durante el ejercicio.',
                'categoria': 'Ropa y Accesorios',
                'precio': Decimal('29.99'),
                'stock': 45,
                'stock_minimo': 10,
                'codigo_barras': 'NIK-DRIF-BLK-L',
                'imagen': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center'
            },
            {
                'nombre': 'Jeans Levi\'s 501',
                'descripcion': 'Jeans clásicos Levi\'s 501 Original Fit, confeccionados en denim 100% algodón con corte recto tradicional.',
                'categoria': 'Ropa y Accesorios',
                'precio': Decimal('89.99'),
                'stock': 32,
                'stock_minimo': 8,
                'codigo_barras': 'LEV-501-BLU-32',
                'imagen': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop&crop=center'
            },
            
            # Hogar y Jardín
            {
                'nombre': 'Aspiradora Dyson V15',
                'descripcion': 'Aspiradora inalámbrica Dyson V15 Detect con tecnología láser para detectar polvo microscópico y batería de larga duración.',
                'categoria': 'Hogar y Jardín',
                'precio': Decimal('649.99'),
                'stock': 8,
                'stock_minimo': 2,
                'codigo_barras': 'DYS-V15-DET-001',
                'imagen': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop&crop=center'
            },
            {
                'nombre': 'Set de Sartenes Antiadherentes',
                'descripcion': 'Juego de 3 sartenes antiadherentes de diferentes tamaños con recubrimiento cerámico y mangos ergonómicos.',
                'categoria': 'Hogar y Jardín',
                'precio': Decimal('79.99'),
                'stock': 22,
                'stock_minimo': 5,
                'codigo_barras': 'KIT-SART-CER-3PC',
                'imagen': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&crop=center'
            },
            
            # Deportes y Fitness
            {
                'nombre': 'Zapatillas Nike Air Max 270',
                'descripcion': 'Zapatillas deportivas Nike Air Max 270 con amortiguación Air Max visible y diseño moderno para uso diario.',
                'categoria': 'Deportes y Fitness',
                'precio': Decimal('149.99'),
                'stock': 28,
                'stock_minimo': 6,
                'codigo_barras': 'NIK-AM270-WHT-42',
                'imagen': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop&crop=center'
            },
            {
                'nombre': 'Mancuernas Ajustables 20kg',
                'descripcion': 'Par de mancuernas ajustables de 5 a 20kg cada una, ideales para entrenamiento en casa con sistema de ajuste rápido.',
                'categoria': 'Deportes y Fitness',
                'precio': Decimal('199.99'),
                'stock': 15,
                'stock_minimo': 3,
                'codigo_barras': 'FIT-MANC-ADJ-20K',
                'imagen': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&crop=center'
            },
            
            # Libros y Medios
            {
                'nombre': 'Libro: "Clean Code"',
                'descripcion': 'Libro "Clean Code: A Handbook of Agile Software Craftsmanship" por Robert C. Martin, guía esencial para programadores.',
                'categoria': 'Libros y Medios',
                'precio': Decimal('42.99'),
                'stock': 35,
                'stock_minimo': 8,
                'codigo_barras': 'LIB-CLEAN-CODE-EN',
                'imagen': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop&crop=center'
            },
            
            # Salud y Belleza
            {
                'nombre': 'Crema Hidratante Facial',
                'descripcion': 'Crema hidratante facial con ácido hialurónico y vitamina E, para todo tipo de piel, 50ml.',
                'categoria': 'Salud y Belleza',
                'precio': Decimal('24.99'),
                'stock': 42,
                'stock_minimo': 10,
                'codigo_barras': 'COS-HIDR-FAC-50ML',
                'imagen': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400&h=400&fit=crop&crop=center'
            },
            
            # Productos con stock bajo para demostrar alertas
            {
                'nombre': 'Auriculares Sony WH-1000XM5',
                'descripcion': 'Auriculares inalámbricos Sony con cancelación de ruido líder en la industria y calidad de sonido excepcional.',
                'categoria': 'Electrónicos',
                'precio': Decimal('399.99'),
                'stock': 3,  # Stock bajo
                'stock_minimo': 5,
                'codigo_barras': 'SON-WH1000XM5-BLK',
                'imagen': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&crop=center'
            },
            
            # Producto agotado
            {
                'nombre': 'PlayStation 5',
                'descripcion': 'Consola de videojuegos Sony PlayStation 5 con unidad de disco, procesador AMD Ryzen Zen 2 y GPU RDNA 2.',
                'categoria': 'Electrónicos',
                'precio': Decimal('499.99'),
                'stock': 0,  # Agotado
                'stock_minimo': 2,
                'codigo_barras': 'SON-PS5-DISC-825GB',
                'imagen': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400&h=400&fit=crop&crop=center'
            },
            
            # Productos adicionales con imágenes reales
            {
                'nombre': 'Smartwatch Apple Watch Series 9',
                'descripcion': 'Reloj inteligente Apple Watch Series 9 con GPS, pantalla Always-On Retina y monitoreo avanzado de salud.',
                'categoria': 'Electrónicos',
                'precio': Decimal('429.99'),
                'stock': 20,
                'stock_minimo': 5,
                'codigo_barras': 'APL-AW9-GPS-45MM',
                'imagen': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop&crop=center'
            },
            {
                'nombre': 'Cafetera Espresso Delonghi',
                'descripcion': 'Cafetera espresso automática DeLonghi con molinillo integrado, sistema de espuma de leche y pantalla táctil.',
                'categoria': 'Hogar y Jardín',
                'precio': Decimal('299.99'),
                'stock': 14,
                'stock_minimo': 3,
                'codigo_barras': 'DEL-ESP-AUTO-001',
                'imagen': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop&crop=center'
            },
            {
                'nombre': 'Bicicleta de Montaña Trek',
                'descripcion': 'Bicicleta de montaña Trek con suspensión completa, cambios Shimano de 21 velocidades y frenos de disco.',
                'categoria': 'Deportes y Fitness',
                'precio': Decimal('899.99'),
                'stock': 6,
                'stock_minimo': 2,
                'codigo_barras': 'TRK-MTB-SUSP-21V',
                'imagen': 'https://images.unsplash.com/photo-1544191696-15693072e0b5?w=400&h=400&fit=crop&crop=center'
            },
            {
                'nombre': 'Perfume Chanel No. 5',
                'descripcion': 'Perfume clásico Chanel No. 5 Eau de Parfum, fragancia icónica y elegante en presentación de 100ml.',
                'categoria': 'Salud y Belleza',
                'precio': Decimal('159.99'),
                'stock': 18,
                'stock_minimo': 4,
                'codigo_barras': 'CHA-NO5-EDP-100ML',
                'imagen': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=400&fit=crop&crop=center'
            },
            {
                'nombre': 'Tablet iPad Air 5ta Gen',
                'descripcion': 'Tablet Apple iPad Air de 5ta generación con chip M1, pantalla Liquid Retina de 10.9 pulgadas y 256GB.',
                'categoria': 'Electrónicos',
                'precio': Decimal('749.99'),
                'stock': 11,
                'stock_minimo': 3,
                'codigo_barras': 'APL-IPAD-AIR5-256',
                'imagen': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop&crop=center'
            }
        ]
        
        productos_creados = 0
        for prod_data in productos_data:
            try:
                categoria = Categoria.objects.get(nombre=prod_data['categoria'])
                producto, created = Producto.objects.get_or_create(
                    codigo_barras=prod_data['codigo_barras'],
                    defaults={
                        'nombre': prod_data['nombre'],
                        'descripcion': prod_data['descripcion'],
                        'categoria': categoria,
                        'precio': prod_data['precio'],
                        'stock': prod_data['stock'],
                        'stock_minimo': prod_data['stock_minimo'],
                        'imagen': prod_data['imagen']
                    }
                )
                if created:
                    productos_creados += 1
                    estado = "🔴 AGOTADO" if producto.stock == 0 else "🟡 BAJO STOCK" if producto.stock <= producto.stock_minimo else "🟢 DISPONIBLE"
                    self.stdout.write(f'✓ Producto creado: {producto.nombre} - {estado}')
                else:
                    self.stdout.write(f'- Producto ya existe: {producto.nombre}')
            except Categoria.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'✗ Categoría no encontrada: {prod_data["categoria"]}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 ¡Proceso completado!'))
        self.stdout.write(self.style.SUCCESS(f'📁 Categorías creadas: {len(categorias_creadas)}'))
        self.stdout.write(self.style.SUCCESS(f'📦 Productos creados: {productos_creados}'))
        self.stdout.write(self.style.SUCCESS(f'\n🚀 Ya puedes usar la aplicación con datos de ejemplo.'))