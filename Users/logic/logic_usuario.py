from ..models import Usuario
from django.contrib.auth import authenticate, login
def get_usuarios():
    queryset = Usuario.objects.all()
    return (queryset)

def create_usuario(form):
    usuario = form.save()
    usuario.save()
    return ()

def login_usuario(request, form):
    login_info = form.cleaned_data['login']
    password = form.cleaned_data['password']
    usuario = authenticate(request, login=login_info, password=password) # Verificar si el usuario existe
    if usuario is not None:
        login(request, usuario) # Iniciar sesión del usuario y persistirlo en la sesión
        return usuario
    else:
        return None