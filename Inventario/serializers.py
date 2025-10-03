from rest_framework import serializers
from .models import Pedido, Producto, Estanteria, Bodega


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

    def get_estanteria_info(self, obj):
        if obj.estanteria:
            return {
                'area_bodega': obj.estanteria.area_bodega,
                'numero_estanteria': obj.estanteria.numero_estanteria,
            }
        return None
    
    def get_bodega_info(self, obj):
        if obj.estanteria and obj.estanteria.bodega:
            bodega = obj.estanteria.bodega
            return {
                'ciudad': bodega.ciudad,
                'direccion': bodega.direccion
            }
        return None
    

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
        



#Pedido

class PedidoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['cliente'] 
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
    

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__' 