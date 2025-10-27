from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from decimal import Decimal

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    ESTADO_STOCK_CHOICES = [
        ('disponible', 'Disponible'),
        ('bajo_stock', 'Bajo Stock'),
        ('agotado', 'Agotado'),
    ]

    nombre = models.CharField(max_length=200, verbose_name="Nombre", db_index=True)
    descripcion = models.TextField(verbose_name="Descripción")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoría")
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Precio",
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.IntegerField(verbose_name="Stock", validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(default=5, verbose_name="Stock Mínimo", validators=[MinValueValidator(0)])
    imagen = models.URLField(blank=True, null=True, verbose_name="URL de Imagen")
    codigo_barras = models.CharField(max_length=50, blank=True, null=True, verbose_name="Código de Barras", unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", db_index=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    activo = models.BooleanField(default=True, verbose_name="Activo", db_index=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['nombre', 'activo']),
            models.Index(fields=['precio']),
            models.Index(fields=['stock']),
        ]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('producto_detalle', kwargs={'pk': self.pk})

    @property
    def estado_stock(self):
        if self.stock == 0:
            return 'agotado'
        elif self.stock <= self.stock_minimo:
            return 'bajo_stock'
        return 'disponible'

    @property
    def estado_stock_display(self):
        estados = {
            'disponible': 'Disponible',
            'bajo_stock': 'Bajo Stock',
            'agotado': 'Agotado'
        }
        return estados.get(self.estado_stock, 'Desconocido')

    @property
    def estado_stock_class(self):
        clases = {
            'disponible': 'success',
            'bajo_stock': 'warning',
            'agotado': 'danger'
        }
        return clases.get(self.estado_stock, 'secondary')

    def tiene_imagen(self):
        return bool(self.imagen)


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    @property
    def total_items(self):
        return sum(item.cantidad for item in self.items.all())

    @property
    def total_precio(self):
        return sum(item.subtotal for item in self.items.all())

    def agregar_producto(self, producto, cantidad=1):
        item, created = CarritoItem.objects.get_or_create(
            carrito=self,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        if not created:
            item.cantidad += cantidad
            item.save()
        return item

    def remover_producto(self, producto):
        try:
            item = self.items.get(producto=producto)
            item.delete()
        except CarritoItem.DoesNotExist:
            pass

    def limpiar(self):
        self.items.all().delete()


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items', verbose_name="Carrito")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad", validators=[MinValueValidator(1)])
    fecha_agregado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha agregado")

    class Meta:
        verbose_name = "Item del Carrito"
        verbose_name_plural = "Items del Carrito"
        unique_together = ('carrito', 'producto')

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio

    def actualizar_cantidad(self, nueva_cantidad):
        if nueva_cantidad <= 0:
            self.delete()
        else:
            self.cantidad = nueva_cantidad
            self.save()