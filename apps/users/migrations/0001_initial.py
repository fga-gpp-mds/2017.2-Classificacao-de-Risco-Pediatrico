# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=150, verbose_name='Nome')),
                ('id_user', models.CharField(max_length=150, unique=True, verbose_name='ID de usuário')),
                ('email', models.EmailField(default='', max_length=254, unique=True, verbose_name='Email do usuário')),
                ('profile', models.IntegerField(choices=[(1, 'Recepcionista'), (2, 'Atendente')], default=0, verbose_name='Perfil')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uf', models.CharField(max_length=50, verbose_name='UF')),
                ('city', models.CharField(max_length=50, verbose_name='Cidade')),
                ('neighborhood', models.CharField(max_length=100, verbose_name='Bairro')),
                ('street', models.CharField(max_length=50, verbose_name='Rua')),
                ('block', models.CharField(max_length=50, verbose_name='Conjunto')),
                ('number', models.CharField(max_length=10, verbose_name='Numero')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nome')),
                ('guardian', models.CharField(help_text='Informe o nome do responsável', max_length=50, verbose_name='Nome do Responsável')),
                ('birth_date', models.DateTimeField(help_text='Informe a data de Nascimento', verbose_name='Data de Nascimento')),
                ('cpf', models.CharField(default='', help_text='Informe o CPF', max_length=11, unique=True, verbose_name='CPF')),
                ('parents_name', models.CharField(help_text='Informe o nome dos pais', max_length=150, unique=True, verbose_name='Nome dos pais')),
            ],
        ),
    ]
