from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ingrese la descripción del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0.')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock