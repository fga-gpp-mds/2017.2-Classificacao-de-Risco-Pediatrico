# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-02 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risk_rating', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinicalstate_10ymore',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='clinicalstate_29d_2m',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='clinicalstate_2m_3y',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='clinicalstate_3y_10y',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='machinelearning_10ymore',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='machinelearning_29d_2m',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='machinelearning_2m_3y',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='machinelearning_3y_10y',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Data'),
        ),
    ]