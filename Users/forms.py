from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'apellido',
            'login',
            'password',
        ]
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'login': 'Login',
            'password': 'Contraseña',
        }