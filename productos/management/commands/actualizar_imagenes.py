from django.core.management.base import BaseCommand
from productos.models import Producto

class Command(BaseCommand):
    help = 'Actualiza las imágenes de los productos existentes con URLs reales'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Actualizando imágenes de productos...'))
        
        # Mapeo de productos con sus nuevas imágenes
        imagenes_productos = {
            'APL-IP15P-128': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop&crop=center',
            'SAM-GS24-256': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&crop=center',
            'APL-MBA-M3-256': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop&crop=center',
            'NIK-DRIF-BLK-L': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center',
            'LEV-501-BLU-32': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop&crop=center',
            'DYS-V15-DET-001': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop&crop=center',
            'KIT-SART-CER-3PC': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&crop=center',
            'NIK-AM270-WHT-42': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop&crop=center',
            'FIT-MANC-ADJ-20K': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&crop=center',
            'LIB-CLEAN-CODE-EN': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop&crop=center',
            'COS-HIDR-FAC-50ML': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400&h=400&fit=crop&crop=center',
            'SON-WH1000XM5-BLK': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&crop=center',
            'SON-PS5-DISC-825GB': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400&h=400&fit=crop&crop=center',
        }
        
        productos_actualizados = 0
        
        for codigo_barras, nueva_imagen in imagenes_productos.items():
            try:
                producto = Producto.objects.get(codigo_barras=codigo_barras)
                producto.imagen = nueva_imagen
                producto.save()
                productos_actualizados += 1
                self.stdout.write(f'✓ Imagen actualizada: {producto.nombre}')
            except Producto.DoesNotExist:
                self.stdout.write(f'✗ Producto no encontrado: {codigo_barras}')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 ¡Actualización completada!'))
        self.stdout.write(self.style.SUCCESS(f'📸 Imágenes actualizadas: {productos_actualizados}'))
        self.stdout.write(self.style.SUCCESS(f'\n🚀 Ahora todos los productos tienen imágenes reales de Unsplash.'))