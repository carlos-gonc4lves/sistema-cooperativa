from django.contrib import admin
from django.utils.html import format_html
from .models import Coletor, Material, Coleta, Caixa
from django.utils.translation import gettext_lazy as _


@admin.register(Coletor)
class ColetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_documento', 'documento_mascarado', 'telefone', 'faz_parte_cooperativa', 'foto')
    search_fields = ('nome', 'documento', 'telefone')
    list_filter = ('tipo_documento', 'faz_parte_cooperativa', 'tipo_conta')

    def foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 8px;" />', obj.foto.url)
        return "Sem foto"
    
    foto.short_description = "Foto"

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco_kg')
    search_fields = ('nome',)

    def get_fields(self, request, obj=None):
        fields = ['nome', 'preco_kg']
        if not request.user.is_superuser and not request.user.groups.filter(name='Financeiro').exists():
            fields.remove('preco_kg')
        return fields
        
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and not request.user.groups.filter(name='Financeiro').exists():
            return ['nome']
        return []

@admin.register(Coleta)
class ColetaAdmin(admin.ModelAdmin):
    list_filter = ('data',)
    search_fields = ('coletor__nome', 'material__nome')

    def get_list_display(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='Financeiro').exists():
            return ('id', 'coletor_link', 'material', 'peso', 'valor_total', 'data')
        else:
            return ('id', 'coletor_link', 'material', 'peso', 'data')

    def coletor_link(self, obj):
        if obj.coletor:
            return format_html('<a href="{}">{}</a>', 
                               f'/admin/reciclagem/coletor/{obj.coletor.id}/change/', 
                               obj.coletor.nome)
        return "Sem coletor"
    coletor_link.short_description = "Coletor"

    def get_fields(self, request, obj=None):
        fields = ['coletor', 'material', 'peso', 'valor_total', 'data']
        if not request.user.is_superuser and not request.user.groups.filter(name='Financeiro').exists():
            fields.remove('valor_total')
        return fields

    def get_readonly_fields(self, request, obj=None):
        readonly = ['data']
        return readonly
    
@admin.register(Caixa)
class CaixaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'entrada', 'saida', 'format_saldo')
    list_filter = ('data',)

    def format_saldo(self, obj):
        saldo = obj.saldo
        cor = 'green' if saldo >= 0 else 'red'
        valor_formatado = f'R$ {saldo:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        return format_html(f'<strong style="color:{cor}">{valor_formatado}</strong>')

    format_saldo.short_description = 'Saldo'

    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name='Financeiro').exists()

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Financeiro').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Financeiro').exists()

    def has_add_permission(self, request):
        has_permission = request.user.is_superuser or request.user.groups.filter(name='Financeiro').exists()
        print(f"Usuário: {request.user.username} Tem permissão para adicionar: {has_permission}")
        return has_permission

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Financeiro').exists()

# Configuração do site Admin
admin.site.site_header = _("Administração")
admin.site.site_title = _("Administração")
admin.site.index_title = _("Painel de Controle")
