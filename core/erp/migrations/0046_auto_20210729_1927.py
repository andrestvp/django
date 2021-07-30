# Generated by Django 2.2.12 on 2021-07-29 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0045_auto_20210729_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='plazo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.Timelimit'),
        ),
        migrations.AlterField(
            model_name='tariff',
            name='descuento',
            field=models.IntegerField(blank=True, null=True, verbose_name='Descuento Precio %'),
        ),
        migrations.AlterField(
            model_name='tariff',
            name='tipo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Tiempo Diferido'),
        ),
    ]
