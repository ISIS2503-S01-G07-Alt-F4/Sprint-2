from django.urls import path
from . import views

urlpatterns = [
    path('producto/crear', views.crear_producto, name='productoCreate'),
    path('bodegas/', views.bodega_list, name='bodegaList'),
    path('seleccionar-bodega/<int:bodega_id>/', views.seleccionar_bodega, name='seleccionarBodega'),
    path("inventario/", views.inventario_view, name="verInventario")
]
