from django.shortcuts import render
from Inventario.logic.logic_inventario import get_bodegas
# Create your views here.
def bodega_list(request):
    bodegas = get_bodegas()
    return render(request, 'Bodega/bodega.html', {'bodegas': bodegas})