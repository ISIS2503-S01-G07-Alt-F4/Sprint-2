from rest_framework import serializers
from .models import Producto, Estanteria, Bodega


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Producto
    """
    estanteria_info = serializers.SerializerMethodField(read_only=True)
    bodega_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id',
            'codigo_barras', 
            'nombre', 
            'tipo', 
            'especificaciones', 
            'precio', 
            'estanteria',
            'estanteria_info',
            'bodega_info'
        ]


class ProductoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer específico para la creación de productos con validaciones adicionales
    """
    class Meta:
        model = Producto
        fields = [
            'codigo_barras', 
            'nombre', 
            'tipo', 
            'especificaciones', 
            'precio', 
            'estanteria'
        ]
        
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        