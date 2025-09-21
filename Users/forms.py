from django import forms
from .models import Usuario

class UsuarioForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    apellido = forms.CharField(label="Apellido", max_length=100)
    login = forms.CharField(label="Login", max_length=100)
    contraseña = forms.CharField(label="Contraseña", max_length=100)
        