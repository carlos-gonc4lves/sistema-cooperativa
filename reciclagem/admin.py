from django.contrib import admin
from .models import Coletor, Material, Coleta, Caixa

@admin.register(Coletor)
class ColetorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'documento')
    search_fields = ('nome', 'documento')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco_kg')
    search_fields = ('nome',)

@admin.register(Coleta)
class ColetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'coletor', 'material', 'peso', 'valor_total', 'data')
    list_filter = ('data',)
    search_fields = ('coletor__nome', 'material__nome')

@admin.register(Caixa)
class CaixaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'entrada', 'saida', 'saldo')
    list_filter = ('data',)

