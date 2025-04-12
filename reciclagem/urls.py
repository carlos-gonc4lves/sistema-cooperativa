from django.urls import path
from . import views

urlpatterns = [
    path('saldos/', views.saldo_por_coletor, name='saldo_por_coletor'),
    path('relatorio-financeiro/', views.relatorio_financeiro, name='relatorio_financeiro'),
]
