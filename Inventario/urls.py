from django.urls import path
from . import views

urlpatterns = [
    path('producto/crear', views.crear_producto, name='productoCreate'),
    path('bodegas/', views.bodega_list, name='bodegaList')
]
