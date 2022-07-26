from django.contrib.auth.models import User
from django.shortcuts import render, redirect #importa o redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required # apos importar so ira ter acesso a genda se estiver logado
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

# Create your views here.
# def index(request):  #importa a redirect
#     return redirect('/agenda/')  #funciona como se fosse um default e sempre ir para a agenda

def login_user(request):#tela de login para quando nao estiver logado
    return render(request, 'login.html')

def logout_user(request): #criando para sair da conta do usuario
    logout(request)
    return redirect('/')

def submit_login(request): #verificando o login
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else: #caso o usuario nao exista ou estiver errado
            messages.error(request, " Usuario ou senha invalido.")
    return redirect('/')

@login_required(login_url='/login/') #chama a importacao
def lista_eventos(request): #reenderizar para pagina html que foi criada em templates
    usuario = request.user #filtar por usuario
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual)#filtar por usuario, caso nao queria filtar por usuario colque .all()
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            # evento = Evento.objects.get(id=id_evento) #faz a edicao com validacao
            # if evento.usuario == usuario:
            #     evento.titulo = titulo,
            #     evento.descricao = descricao,
            #     evento.data_evento = data_evento
            #     evento.save()
            Evento.objects.filter(id=id_evento).update(titulo=titulo, #aqui e outra forma de fazer a edicao porem sem validacao
                                                       data_evento=data_evento,
                                                       descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  usuario=usuario)
    return redirect('/agenda/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404
    return redirect('/agenda/')


def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False)
