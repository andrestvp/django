# Generated by Django 2.2.12 on 2021-08-04 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0015_auto_20210804_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='tax',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.Impuesto'),
        ),
    ]
