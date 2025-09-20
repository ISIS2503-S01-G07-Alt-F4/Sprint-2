from Inventario.models import Bodega, Estanteria, HistorialMovimiento, Item, Producto

def crear_bodega(data):
    bodega = Bodega.objects.create(**data)
    return bodega

def get_bodegas():
    queryset = Bodega.objects.all()
    return (queryset)

def crear_estanteria(data):
    estanteria = Estanteria.objects.create(**data)
    return estanteria

def registrar_producto(data):
    producto = Producto.objects.create(**data)
    return producto

def registrar_item(data):
    item = Item.objects.create(**data)
    return item
