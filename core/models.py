from django.db import models
from django.contrib.auth.models import User #importando o usuario

# Create your models here.

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True) #pode esta em branco e ser nulo
    data_evento = models.DateTimeField(verbose_name='Data do Evento') #Alterando o nome do tiutlo com verbose_name
    data_criacao = models.DateTimeField(auto_now=True) #para pegar a hora que foi criado o evento
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #se o ususario dono da aplicacao for excluido, exclui todos os outros com on_delte

    class Meta: #informando qual o nome do banco
        db_table = 'evento'

    def __str__(self): #colocando para aparecer o nome do evento
        return self.titulo

