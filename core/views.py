from django.shortcuts import render
from core.models import Evento

# Create your views here.
# def index(request):  #importa a redirect
#     return redirect('/agenda/')  #funciona como se fosse um default e sempre ir para a agenda

def lista_eventos(request): #reenderizar para pagina html que foi criada em templates
    # usuario = request.user #filtar por usuario
    evento = Evento.objects.all() #filter(usuario=usuario) #filtar por usuario
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)