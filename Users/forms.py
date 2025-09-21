from django import forms
from .models import Usuario

from django.forms import ModelForm
from .models import Usuario

class UsuarioLoginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
        
from Inventario.models import Bodega

class UsuarioCreateForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    apellido = forms.CharField(label="Apellido", max_length=100)
    login = forms.CharField(label="Login", max_length=100)
    contraseña = forms.CharField(label="Contraseña", max_length=100)
    rol = forms.ChoiceField(label="Rol", choices=[('JefeBodega', 'JefeBodega'), ('Operario', 'Operario'), ('Usuario', 'Usuario')])
    bodega = forms.ModelChoiceField(label="Bodega", queryset=Bodega.objects.all(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        bodega = cleaned_data.get('bodega')
        if rol == 'JefeBodega' and not bodega:
            self.add_error('bodega', 'Debe seleccionar una bodega para el Jefe de Bodega.')
        return cleaned_data