from django.shortcuts import render
from django.db.models import Sum
from .models import Coletor, Coleta
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from decimal import Decimal


# Checa se o usuário NÃO é operador básico
def nao_operador_basico(user):
    return not user.groups.filter(name="Operador Básico").exists()

@login_required
def saldo_por_coletor(request):
    filtro = request.GET.get('filtro', '').strip().lower()

    cooperados = Coletor.objects.filter(faz_parte_cooperativa=True)
    municipes = Coletor.objects.filter(faz_parte_cooperativa=False)

    if filtro:
        cooperados = cooperados.filter(nome__icontains=filtro)
        municipes = municipes.filter(nome__icontains=filtro)

    eh_operador_basico = request.user.groups.filter(name="Operador Básico").exists()

    saldos_cooperados = []
    saldos_municipes = []

    for coletor in cooperados:
        total = Coleta.objects.filter(coletor=coletor).aggregate(soma=Sum('valor_total'))['soma'] or 0
        saldos_cooperados.append({
            'nome': coletor.nome,
            'documento': None if eh_operador_basico else coletor.documento_mascarado,
            'saldo': None if eh_operador_basico else total
        })

    for coletor in municipes:
        total = Coleta.objects.filter(coletor=coletor).aggregate(soma=Sum('valor_total'))['soma'] or 0
        saldos_municipes.append({
            'nome': coletor.nome,
            'documento': None if eh_operador_basico else coletor.documento_mascarado,
            'saldo': None if eh_operador_basico else total
        })

    context = {
        'saldos_cooperados': saldos_cooperados,
        'saldos_municipes': saldos_municipes,
        'eh_operador_basico': eh_operador_basico,
        'filtro': request.GET.get('filtro', ''),
    }

    return render(request, 'reciclagem/saldo_por_coletor.html', context)

from django.shortcuts import render
from datetime import date
from decimal import Decimal
from .models import Coleta, Coletor  # Certifique-se de importar o modelo Coletor

# RELATÓRIO FINANCEIRO COM RESTRIÇÃO A OPERADOR BÁSICO
@login_required
@user_passes_test(nao_operador_basico)
def relatorio_financeiro(request):
    hoje = date.today()
    inicio_mes = date(hoje.year, hoje.month, 1)
    inicio_ano_anterior = date(hoje.year - 1, 1, 1)
    fim_ano_anterior = date(hoje.year - 1, 12, 31)

    # Total arrecadado no mês atual
    arrecadacao_mes = Coleta.objects.filter(data__gte=inicio_mes).aggregate(total=Sum('valor_total'))['total'] or 0
    fundo_reserva_mes = arrecadacao_mes * Decimal('0.10')
    restante_mes = arrecadacao_mes - fundo_reserva_mes

    # Total arrecadado no ano anterior
    arrecadacao_ano_anterior = Coleta.objects.filter(data__range=(inicio_ano_anterior, fim_ano_anterior)).aggregate(total=Sum('valor_total'))['total'] or 0
    fundo_reserva_anual = arrecadacao_ano_anterior * Decimal('0.10')
    fates = fundo_reserva_anual * Decimal('0.05')
    restante_anual = arrecadacao_ano_anterior - fundo_reserva_anual

    coletores = Coletor.objects.all()  # Pega todos os coletores

    contexto = {
        'arrecadacao_mes': arrecadacao_mes,
        'fundo_reserva_mes': fundo_reserva_mes,
        'restante_mes': restante_mes,
        'arrecadacao_ano_anterior': arrecadacao_ano_anterior,
        'fundo_reserva_anual': fundo_reserva_anual,
        'fates': fates,
        'restante_anual': restante_anual,
        'coletores': coletores,  # Adiciona os coletores ao contexto
    }

    return render(request, 'reciclagem/relatorio_financeiro.html', contexto)
