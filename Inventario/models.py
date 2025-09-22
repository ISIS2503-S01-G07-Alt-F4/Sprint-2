from django.db import models
# Create your models here.

class Bodega(models.Model):
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.ciudad} - {self.direccion}"
    
class Estanteria(models.Model):
    area_bodega = models.CharField(max_length=100)
    numero_estanteria = models.CharField(max_length=50)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)  
    
    def __str__(self):
        return f"#{self.numero_estanteria} - Área {self.area_bodega}"
    
class Producto(models.Model):
    codigo_barras = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    especificaciones = models.TextField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    estanteria = models.ForeignKey(Estanteria, on_delete=models.DO_NOTHING)  # No on_delete porque es agregación
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo_barras})"
 
class HistorialMovimiento(models.Model):
    operario_responsable = models.ForeignKey('Users.Operario', on_delete=models.DO_NOTHING)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(max_length=50, choices=[('Ingreso', 'Ingreso'), ('Retiro', 'Retiro')])
       
class Item(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  
    sku = models.CharField(max_length=100, unique=True) # identificador único
    ingreso = models.ForeignKey(HistorialMovimiento, on_delete=models.CASCADE, related_name='ingresos')
    retiro = models.ForeignKey(HistorialMovimiento, on_delete=models.SET_NULL, null=True, blank=True)
    
