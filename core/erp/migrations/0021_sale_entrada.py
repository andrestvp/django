# Generated by Django 2.2.12 on 2021-07-21 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0020_sale_plazo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='entrada',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
