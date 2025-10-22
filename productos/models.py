from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
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