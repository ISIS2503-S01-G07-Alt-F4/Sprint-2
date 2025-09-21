from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('crearusuario/', csrf_exempt(views.usuario_create), name='usuarioCreate'),
    path('login/', csrf_exempt(views.usuario_login), name='usuarioLogin'),
]
