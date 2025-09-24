from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .logic.logic_api import procesar_creacion_producto_completa


@api_view(['POST'])
@permission_classes([AllowAny]) 
@csrf_exempt
def crear_producto_api(request):
    """
    Endpoint para crear un nuevo producto
    
    Parámetros requeridos en el body JSON:
    - username: Usuario para autenticación
    - password: Contraseña para autenticación
    - codigo_barras: Código único del producto
    - nombre: Nombre del producto
    - tipo: Tipo de producto
    - especificaciones: Especificaciones técnicas
    - precio: Precio del producto
    - estanteria: ID de la estantería donde se ubicará
    - bodega_seleccionada (opcional): ID de la bodega para operarios
    
    Ejemplo de request:
    {
        "username": "operario1",
        "password": "password123",
        "codigo_barras": "1234567890123",
        "nombre": "Chaqueta de Prueba",
        "tipo": "Prueba",
        "especificaciones": "Chaqueta de prueba, talla M, color rojo",
        "precio": "1500000.00",
        "estanteria": 1,
        "bodega_seleccionada": 2 # Solo para operarios
    }
    """
    return procesar_creacion_producto_completa(request.data)

@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok"}, status=200)