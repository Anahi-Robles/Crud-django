from django import forms
# Importa el formulario de creación de usuarios
from django.contrib.auth.forms import UserCreationForm
# Importa el modelo User
from django.contrib.auth.models import User
from .models import Producto, Categoria

# --- Ahora empieza tu clase ---
class RegistroForm(UserCreationForm):
    # ...
    # Añadimos el campo de email, que no viene por defecto
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'correo@ejemplo.com'
        }),
        help_text="Requerido. Escribe un email válido."
    )

    class Meta:
        model = User
        # Definimos los campos que queremos en el formulario
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadimos las clases de Bootstrap a los campos que ya existen
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Elige un nombre de usuario'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Escribe una contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Repite la contraseña'
        })


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'precio', 'stock', 'stock_minimo', 'imagen', 'codigo_barras']
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
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '5'
            }),
            'imagen': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://ejemplo.com/imagen.jpg'
            }),
            'codigo_barras': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de barras (opcional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(activo=True)
        self.fields['categoria'].empty_label = "Seleccione una categoría"

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0.')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock

    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo is not None and stock_minimo < 0:
            raise forms.ValidationError('El stock mínimo no puede ser negativo.')
        return stock_minimo

    def clean_codigo_barras(self):
        codigo_barras = self.cleaned_data.get('codigo_barras')
        if codigo_barras:
            # Verificar que no exista otro producto con el mismo código
            existing = Producto.objects.filter(codigo_barras=codigo_barras, activo=True)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError('Ya existe un producto con este código de barras.')
        return codigo_barras

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la categoría (opcional)'
            }),
        }