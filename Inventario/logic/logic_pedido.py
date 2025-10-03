from Inventario.logic.logic_api import autenticar_usuario_api
from Inventario.models import Pedido
from django.contrib.auth import authenticate
from Inventario.serializers import PedidoCreateSerializer, PedidoSerializer
from rest_framework import status
from rest_framework.response import Response


def obtener_pedido(id : int):
    try:
        pedido = Pedido.objects.get(id = id)
        return pedido
    except Pedido.DoesNotExist:
        return None
    

def registrar_pedido(data: dict) -> Pedido:
    pedido = Pedido.objects.create(**data)
    return pedido


def verificar_permisos_pedido(usuario):
    """
    Verifica si el usuario tiene permisos para crear pedidos
    """
    if not usuario.is_authenticated:
        return False, "Usuario no autenticado"
    
    if usuario.rol not in ['Operario']:
        return False, "No tienes permisos para crear pedidos"
    
    return True, "OK"

def procesar_creacion_pedido_completa(request_data):
    """
    Procesa la creación completa de un pedido desde la API
    Coherente con el sistema de autenticación usado en las vistas web
    """
    try:
        # 1. Autenticar usuario usando username/password en el body (como en las vistas web)
        username = request_data.get('username')
        password = request_data.get('password')
        
        user, error_response = autenticar_usuario_api(username, password)
        if error_response:
            return error_response
        
        # 2. Verificar permisos
        tiene_permisos, mensaje = verificar_permisos_pedido(user)
        if not tiene_permisos:
            return Response({'error': mensaje,'codigo': 'INSUFFICIENT_PERMISSIONS'}, status=status.HTTP_403_FORBIDDEN)

        # 3. Validar datos del producto
        pedido_data, campos_faltantes = validar_datos_pedido(request_data)
        
        if campos_faltantes != []:
            return Response({'error': f'Campos requeridos faltantes: {", ".join(campos_faltantes)}','codigo': 'MISSING_FIELDS','campos_faltantes': campos_faltantes}, status=status.HTTP_400_BAD_REQUEST)
        
      
        # 4. Crear pedido
        success_response, error_response = crear_pedido_logica(user, pedido_data)
        if error_response:
            return error_response
        return success_response
        
    except Exception as e:
        return Response({'error': f'Error interno del servidor: {str(e)}','codigo': 'INTERNAL_ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


def crear_pedido_logica(usuario, producto_data):
    """
    Lógica principal para crear un producto usando los serializers
    """
    try:
        # Crear el serializer con el usuario para validaciones
        serializer = PedidoCreateSerializer(data=producto_data, usuario=usuario)
        if serializer.is_valid():
            # Crear el pedido
            pedido = serializer.save()
            # Serializar la respuesta con información completa
            response_serializer = PedidoSerializer(pedido)
            return Response({'mensaje': 'Pedido creado exitosamente', 'producto': response_serializer.data, 'codigo': 'SUCCESS'}, status=status.HTTP_201_CREATED), None
        else:
            return None, Response({'error': 'Datos inválidos','errores': serializer.errors,'codigo': 'VALIDATION_ERROR'}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return None, Response({'error': f'Error interno del servidor: {str(e)}','codigo': 'INTERNAL_ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def validar_datos_pedido(request_data):
    """
    Valida que todos los campos requeridos estén presentes
    """
    producto_data = {
        'cliente': request_data.get('cliente'),
        
    }
    
    campos_requeridos = ['cliente']
    campos_faltantes = []
    
    for campo in campos_requeridos:
        if not producto_data.get(campo):
            campos_faltantes.append(campo)    
            
    return producto_data, campos_faltantes

