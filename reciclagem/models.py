from django.db import models

class Coletor(models.Model):
    nome = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome

class Material(models.Model):
    nome = models.CharField(max_length=100)
    preco_kg = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome

class Coleta(models.Model):
    coletor = models.ForeignKey(Coletor, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    peso = models.FloatField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    data = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.peso and self.material:
            self.valor_total = self.peso * self.material.preco_kg
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.coletor} - {self.material} - {self.peso}kg"

class Caixa(models.Model):
    data = models.DateField(auto_now_add=True)
    entrada = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    saida = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Saldo: {self.saldo}"
