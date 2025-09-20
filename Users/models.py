from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100, default="Sin nombre") 
    apellido = models.CharField(max_length=100, blank=True)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    
class Operario(Usuario):
    rol = models.CharField(max_length=50)