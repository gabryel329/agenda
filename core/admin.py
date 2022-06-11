from django.contrib import admin
from core.models import Evento

# Register your models here.

class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_evento', 'data_criacao') #colocando os titulos da coluna para aparecer
    list_filter = ('titulo', 'usuario') #colocando filtro

admin.site.register(Evento, EventoAdmin)
