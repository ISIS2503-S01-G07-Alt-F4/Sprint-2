from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from Inventario.forms import ProductoForm
from Inventario.logic.logic_inventario import get_bodegas
from Inventario.logic.logic_producto import registrar_producto
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
    if request.user.is_authenticated:
        rol = request.user.rol
    else:
        rol = None
        
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            registrar_producto(data)
            return HttpResponseRedirect(reverse('productoCreate'))
        else:
            print(form.errors)
    else:
        form = ProductoForm()
    context = {'form': form, 'rol': rol}
    return render(request, 'Producto/crearProducto.html', context)