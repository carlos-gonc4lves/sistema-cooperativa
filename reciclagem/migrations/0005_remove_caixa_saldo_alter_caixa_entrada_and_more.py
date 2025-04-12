# Generated by Django 5.2 on 2025-04-12 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reciclagem', '0004_remove_coletor_conta_para_deposito_coletor_agencia_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caixa',
            name='saldo',
        ),
        migrations.AlterField(
            model_name='caixa',
            name='entrada',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='saida',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
