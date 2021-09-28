# Generated by Django 2.2.12 on 2021-09-03 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0003_pricelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='entrada',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='sale',
            name='plazo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pos.PriceList'),
        ),
    ]
