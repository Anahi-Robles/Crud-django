from django.contrib import admin
from .models import Producto, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información de la Categoría', {
            'fields': ('nombre', 'descripcion', 'activo')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'estado_stock_display', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'categoria', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion', 'codigo_barras']
    list_editable = ['precio', 'stock', 'activo']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'estado_stock_display']
    autocomplete_fields = ['categoria']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'categoria')
        }),
        ('Detalles Comerciales', {
            'fields': ('precio', 'stock', 'stock_minimo', 'estado_stock_display')
        }),
        ('Información Adicional', {
            'fields': ('codigo_barras', 'imagen', 'activo'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def estado_stock_display(self, obj):
        return obj.estado_stock_display
    estado_stock_display.short_description = 'Estado Stock'
    estado_stock_display.admin_order_field = 'stock'