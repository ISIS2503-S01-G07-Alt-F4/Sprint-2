from django.forms import ModelForm
from .models import Producto

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_barras', 'nombre', 'tipo', 'especificaciones', 'precio', 'estanteria']