from django.db import models
from django.urls import reverse

class Producto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.IntegerField(verbose_name="Stock")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('producto_detalle', kwargs={'pk': self.pk})