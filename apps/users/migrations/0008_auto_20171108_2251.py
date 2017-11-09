# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_patient_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(0, 'Sexo indefinido'), (1, 'Feminino'), (2, 'Masculino')], default=0, verbose_name='Classification'),
        ),
    ]