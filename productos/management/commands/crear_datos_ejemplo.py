from django.core.management.base import BaseCommand
from productos.models import Producto

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para el CRUD de productos'

    def handle(self, *args, **options):
        productos_ejemplo = [
            {
                'nombre': 'Laptop Dell Inspiron',
                'descripcion': 'Laptop Dell Inspiron 15 con procesador Intel Core i5, 8GB RAM, 256GB SSD. Ideal para trabajo y estudio.',
                'precio': 15999.99,
                'stock': 25
            },
            {
                'nombre': 'Mouse Inalámbrico Logitech',
                'descripcion': 'Mouse inalámbrico ergonómico con sensor óptico de alta precisión. Batería de larga duración.',
                'precio': 599.99,
                'stock': 150
            },
            {
                'nombre': 'Teclado Mecánico RGB',
                'descripcion': 'Teclado mecánico gaming con switches azules, retroiluminación RGB personalizable y teclas anti-ghosting.',
                'precio': 2499.99,
                'stock': 45
            },
            {
                'nombre': 'Monitor 24" Full HD',
                'descripcion': 'Monitor LED de 24 pulgadas con resolución Full HD 1920x1080, panel IPS y conectividad HDMI/VGA.',
                'precio': 3299.99,
                'stock': 30
            },
            {
                'nombre': 'Auriculares Bluetooth',
                'descripcion': 'Auriculares inalámbricos con cancelación de ruido activa, 30 horas de batería y micrófono integrado.',
                'precio': 1899.99,
                'stock': 75
            },
            {
                'nombre': 'Webcam HD 1080p',
                'descripcion': 'Cámara web con resolución Full HD, micrófono incorporado y enfoque automático. Perfecta para videollamadas.',
                'precio': 899.99,
                'stock': 60
            },
            {
                'nombre': 'Disco Duro Externo 1TB',
                'descripcion': 'Disco duro portátil de 1TB con conexión USB 3.0, diseño compacto y resistente a golpes.',
                'precio': 1299.99,
                'stock': 40
            },
            {
                'nombre': 'Tablet Android 10"',
                'descripcion': 'Tablet con pantalla de 10 pulgadas, procesador octa-core, 4GB RAM, 64GB almacenamiento y Android 12.',
                'precio': 4999.99,
                'stock': 20
            }
        ]

        productos_creados = 0
        for producto_data in productos_ejemplo:
            producto, created = Producto.objects.get_or_create(
                nombre=producto_data['nombre'],
                defaults=producto_data
            )
            if created:
                productos_creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Producto creado: {producto.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Producto ya existe: {producto.nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n¡Proceso completado! Se crearon {productos_creados} productos nuevos.')
        )