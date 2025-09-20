from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('crearusuario/', csrf_exempt(views.create_usuario), name='usuarioCreate'),
]
