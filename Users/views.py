from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from Users.forms import UsuarioForm
#from .logic.logic_usuario import create_usuario

# Create your views here.
def usurario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Usuario creado correctamente")
            return HttpResponseRedirect(reverse('usuarioCreate'))
        else:
            print(form.errors)
    else:
        form = UsuarioForm()
    
    context = {
        'form': form
    }
    return render(request, 'Usuario/usuarioCreate.html', context)