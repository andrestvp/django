# Generated by Django 2.2.12 on 2021-07-16 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0012_auto_20210716_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='state',
        ),
        migrations.AddField(
            model_name='purchase',
            name='plazo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.Timelimit'),
        ),
    ]
