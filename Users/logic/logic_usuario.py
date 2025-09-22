from ..models import Usuario, JefeBodega, Operario
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
def get_usuarios():
    queryset = Usuario.objects.all()
    return (queryset)

def create_usuario(data):
    modelos = {
        'Usuario': Usuario,
        'JefeBodega': JefeBodega,
        'Operario': Operario
    }
    modelo = modelos.get(data['rol'])
    
    try:
        datos_usuario = {
            'login': data['login'],
            'password': data['contraseña'],
            'nombre': data['nombre'],
            'apellido': data['apellido'],
            'rol': data['rol']
        }
        
        if data['rol'] == 'JefeBodega':
            # JefeBodega: tomar la primera bodega de la lista
            bodegas_seleccionadas = data.get('bodegas', [])
            if bodegas_seleccionadas:
                datos_usuario['bodega'] = bodegas_seleccionadas[0]
            usuario = modelo.objects.create_user(**datos_usuario)
            
        elif data['rol'] == 'Operario':
            usuario = modelo.objects.create_user(**datos_usuario)
            bodegas_seleccionadas = data.get('bodegas', [])
            if bodegas_seleccionadas:
                usuario.bodega.set(bodegas_seleccionadas) 
            
        else:
            usuario = modelo.objects.create_user(**datos_usuario)
            
        print("Usuario creado correctamente")
        return usuario
        
    except Exception as e:
        print(f"Error creando usuario: {e}")
        return None


def login_usuario(request, form):
    login_info = form.cleaned_data['login']
    password = form.cleaned_data['password']
    usuario = authenticate(request, login=login_info, password=password) # Verificar si el usuario existe
    if usuario is not None:
        login(request, usuario) # Iniciar sesión del usuario y persistirlo en la sesión
        return usuario
    else:
        return None
    
def cerrar_sesion(request):
    logout(request)
    