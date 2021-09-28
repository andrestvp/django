# Generated by Django 2.2.12 on 2021-09-11 21:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0023_sale_subtotaltres'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.IntegerField(default=0)),
                ('concepto', models.CharField(max_length=150, verbose_name='Nombre')),
                ('payment_condition', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Credito')], default='contado', max_length=50)),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('end_credit', models.DateField(default=datetime.datetime.now)),
                ('state', models.CharField(choices=[('Enviado', 'Enviado'), ('Anulado', 'Anulado'), ('Aprobado', 'Aprobado'), ('Asignar Series', 'Asignar Series'), ('Rechazado', 'Rechazado')], default='Enviado', max_length=50)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.Provider')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.Sucursal')),
            ],
            options={
                'verbose_name': 'Orden de Compra',
                'verbose_name_plural': 'Ordenes de Compra',
                'ordering': ['-id'],
                'permissions': (('view_purchaseorder', 'Can view OrdenCompra'), ('add_purchaseorder', 'Can add OrdenCompra'), ('delete_purchaseorder', 'Can delete OrdenCompra')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.IntegerField(default=0)),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('state', models.CharField(choices=[('Enviado', 'Enviado'), ('Anulado', 'Anulado'), ('Aprobado', 'Aprobado'), ('Asignar Series', 'Asignar Series'), ('Rechazado', 'Rechazado')], default='Enviado', max_length=50)),
            ],
            options={
                'verbose_name': 'Solicitud de Compra',
                'verbose_name_plural': 'Solicitudes de Compras',
                'permissions': (('view_purchaserequest', 'Can view SolicitudCompra'), ('add_purchaserequest', 'Can add SolicitudCompra'), ('delete_purchaserequest', 'Can delete SolicitudCompra')),
                'default_permissions': (),
            },
        ),
        migrations.AlterModelOptions(
            name='quotationsale',
            options={'default_permissions': (), 'ordering': ['-id'], 'permissions': (('view_sale', 'Can view Solicitud de Ventas'), ('add_sale', 'Can add Solicitud de  Ventas'), ('delete_sale', 'Can delete Solicitud de Ventas')), 'verbose_name': 'Solicitud de Venta', 'verbose_name_plural': 'Solicitud de Ventas'},
        ),
        migrations.CreateModel(
            name='PurchaseRequestDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.Product')),
                ('purchaserequest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.PurchaseRequest')),
            ],
            options={
                'verbose_name': 'Detalle de solicitud de Compra',
                'verbose_name_plural': 'Detalle de solicitud de Compra',
                'ordering': ['-id'],
                'permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.Product')),
                ('purchaseorder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.PurchaseOrder')),
            ],
            options={
                'verbose_name': 'Detalle de Compra',
                'verbose_name_plural': 'Detalle de Compras',
                'ordering': ['-id'],
                'permissions': (),
            },
        ),
    ]
