# Generated by Django 2.2.12 on 2021-08-31 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0058_auto_20210831_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='purchasecost',
        ),
    ]
