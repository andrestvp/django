# Generated by Django 2.2.12 on 2021-07-14 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='email',
            field=models.EmailField(max_length=30, unique=True, verbose_name='Correo'),
        ),
    ]
