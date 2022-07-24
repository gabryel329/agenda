from django.shortcuts import render, redirect #importa o redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required # apos importar so ira ter acesso a genda se estiver logado
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
    evento = Evento.objects.filter(usuario=usuario)#filtar por usuario, caso nao queria filtar por usuario colque .all()
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    return render(request, 'evento.html')

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        Evento.objects.create(titulo=titulo,
                              data_evento=data_evento,
                              descricao=descricao,
                              usuario=usuario)
    return redirect('/agenda/')
