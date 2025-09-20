from django.db import models

from Inventario.models import Bodega
# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100, default="Sin nombre") 
    apellido = models.CharField(max_length=100, blank=True)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    rol = models.CharField(max_length=50, default="Usuario") 
    
class Operario(Usuario):
    bodega = models.ManyToManyField('Inventario.Bodega')
class JefeBodega(Usuario):
    bodega = models.ForeignKey('Inventario.Bodega', on_delete=models.DO_NOTHING) 

                                                        