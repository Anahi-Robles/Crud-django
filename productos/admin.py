from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Detalles Comerciales', {
            'fields': ('precio', 'stock', 'activo')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )