from django.urls import path
from . import views

urlpatterns = [
    path('bodegas/', views.bodega_list)
]
