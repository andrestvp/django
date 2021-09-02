# Generated by Django 2.2.12 on 2021-08-03 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0004_auto_20210803_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.Category', verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='product',
            name='codigo',
            field=models.CharField(max_length=150, null=True, unique=True, verbose_name='Código'),
        ),
        migrations.AlterField(
            model_name='product',
            name='currentcost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Costo Actual'),
        ),
        migrations.AlterField(
            model_name='product',
            name='datasheet',
            field=models.CharField(max_length=250, null=True, verbose_name='Ficha Técnica'),
        ),
        migrations.AlterField(
            model_name='product',
            name='detail',
            field=models.CharField(max_length=250, null=True, verbose_name='Detalle'),
        ),
        migrations.AlterField(
            model_name='product',
            name='maxstock',
            field=models.IntegerField(default=0, verbose_name='Stock Máximo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='minstock',
            field=models.IntegerField(default=0, verbose_name='Stock Mínimo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='product',
            name='purchasecost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Costo Compra'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pvp',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de venta'),
        ),
        migrations.AlterField(
            model_name='product',
            name='standardcost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Costo Estándar'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=2, verbose_name='Stock'),
        ),
        migrations.AlterField(
            model_name='product',
            name='suc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.Sucursal', verbose_name='Sucursal'),
        ),
        migrations.CreateModel(
            name='Secuences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Secuencia')),
                ('secuenceValue', models.IntegerField(blank=True, null=True, unique=True, verbose_name='Secuencia')),
                ('suc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.Sucursal', verbose_name='Sucursal')),
            ],
            options={
                'verbose_name': 'Secuencia',
                'verbose_name_plural': 'Secuencias',
                'ordering': ['id'],
            },
        ),
    ]
