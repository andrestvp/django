# Generated by Django 2.2.12 on 2021-07-15 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0007_auto_20210715_1427'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detpurchase',
            options={'ordering': ['id'], 'verbose_name': 'Detalle de Purchase', 'verbose_name_plural': 'Detalle de Purchase'},
        ),
    ]
