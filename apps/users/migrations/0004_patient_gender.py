# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 00:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20171107_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(0, 'Sexo Indefinido'), (1, 'Masculino'), (2, 'Feminino')], default=0, verbose_name='Classification'),
        ),
    ]