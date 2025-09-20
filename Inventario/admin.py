from django.contrib import admin
from .models import Bodega, Estanteria, Producto, Item, HistorialMovimiento
# Register your models here.
admin.site.register(Bodega)
admin.site.register(Estanteria)
admin.site.register(Producto)
admin.site.register(Item)
admin.site.register(HistorialMovimiento)