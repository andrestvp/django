# Generated by Django 2.2.12 on 2021-09-16 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0035_auto_20210916_0727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaserequest',
            name='subtotaltres',
        ),
    ]
