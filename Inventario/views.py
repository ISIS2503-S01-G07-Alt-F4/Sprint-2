from django.shortcuts import render
from Inventario.logic.logic_inventario import get_bodegas
# Create your views here.
def bodega_list(request):
    if request.user.is_authenticated:
        rol = request.user.rol
    else:
        rol = None
    print(request.user)
    bodegas = get_bodegas()
    return render(request, 'Bodega/bodega.html', {'bodegas': bodegas, 'rol': rol})


def crear_producto(request):
    return render(request, 'Producto/crearProducto.html')