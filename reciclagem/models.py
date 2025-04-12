from django.db import models
from decimal import Decimal


class Coletor(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CPF', 'CPF'),
        ('RG', 'RG'),
        ('CNH', 'CNH'),
    ]

    TIPO_CONTA_CHOICES = [
        ('corrente', 'Conta Corrente'),
        ('poupanca', 'Poupança'),
    ]

    nome = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES)
    documento = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to='fotos_coletores/', null=True, blank=True)
    faz_parte_cooperativa = models.BooleanField(default=False)

    # Dados adicionais
    endereco = models.TextField()
    telefone = models.CharField(max_length=20)
    email = models.EmailField("E-mail", null=True, blank=True)
    
    # Conta para depósito
    tipo_conta = models.CharField(max_length=10, choices=TIPO_CONTA_CHOICES, default='corrente')
    agencia = models.CharField(max_length=10, default='0000')
    numero_conta = models.CharField(max_length=20, default='000000')
    banco = models.CharField(max_length=50, default='Não informado')


    class Meta:
        verbose_name = "Coletor"
        verbose_name_plural = "Coletores"

    def __str__(self):
        return self.nome

    @property
    def documento_mascarado(self):
        """Oculta parte do CPF (formato: 123.456.789-00)"""
        if len(self.documento) == 14 and self.documento.count('.') == 2 and '-' in self.documento:
            return f"{self.documento[:3]}.XXX.XXX-{self.documento[-2:]}"
        return self.documento
    
class Material(models.Model):
    nome = models.CharField(max_length=100)
    preco_kg = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"

    def __str__(self):
        return self.nome
        

class Coleta(models.Model):
    coletor = models.ForeignKey(Coletor, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    peso = models.FloatField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    data = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Coleta"
        verbose_name_plural = "Coletas"

    def save(self, *args, **kwargs):
        if self.peso and self.material:
            self.valor_total = Decimal(str(self.peso)) * self.material.preco_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.coletor} - {self.material} - {self.peso}kg"


class Caixa(models.Model):
    data = models.DateField(auto_now_add=True)
    entrada = models.DecimalField(max_digits=10, decimal_places=2)
    saida = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def saldo(self):
        return self.entrada - self.saida
    
    def __str__(self):
        return f"{self.data} | Saldo: R$ {self.saldo:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    
    class Meta:
       verbose_name = "Caixa"
       verbose_name_plural = "Caixas"

    
