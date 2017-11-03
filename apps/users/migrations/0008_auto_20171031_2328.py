# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-31 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20171031_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='age_range',
            field=models.IntegerField(choices=[(0, '0 até 28 dias'), (1, '29 dias à 3 meses'), (2, '3 meses à 2 anos'), (3, '2 anos à 10 anos'), (4, 'Acima de 10 anos')], default=0, verbose_name='Classification'),
        ),
    ]