# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-02 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_patient_classifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='classifier_id',
            field=models.CharField(blank=True, default='', max_length=150, verbose_name='ID do Classificador'),
        ),
    ]
