# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-12 11:53
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
                ('profile', models.IntegerField(choices=[(1, 'receptionista'), (2, 'Atendente')], default=0, verbose_name='Perfil')),
                ('cep', models.CharField(default='', max_length=8, verbose_name='CEP')),
                ('uf', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='UF')),
                ('city', models.CharField(max_length=50, verbose_name='Cidade')),
                ('neighborhood', models.CharField(max_length=100, verbose_name='Bairro')),
                ('street', models.CharField(max_length=50, verbose_name='Rua')),
                ('block', models.CharField(max_length=50, verbose_name='Conjunto')),
                ('number', models.CharField(max_length=10, verbose_name='Numero')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, default='', max_length=150, verbose_name='Nome')),
                ('comment_receptionist', models.CharField(blank=True, default='', max_length=300, verbose_name='Comentário do receptionista')),
                ('classifier_id', models.CharField(blank=True, default='', max_length=150, verbose_name='ID do Classificador')),
                ('guardian', models.CharField(blank=True, default='', help_text='Informe o nome do responsável', max_length=50, verbose_name='Nome do Responsável')),
                ('birth_date', models.DateField(blank=True, help_text='Informe a data de Nascimento', null=True, verbose_name='Data de Nascimento')),
                ('cpf', models.CharField(blank=True, help_text='Informe o CPF', max_length=14, null=True, unique=True, verbose_name='CPF')),
                ('parents_name', models.CharField(blank=True, default='', help_text='Informe o nome dos pais', max_length=150, verbose_name='Nome dos pais')),
                ('cep', models.CharField(blank=True, help_text='Informe o CEP', max_length=9, null=True, unique=True, verbose_name='CEP')),
                ('uf', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], default='', max_length=2, verbose_name='UF')),
                ('city', models.CharField(blank=True, default='', max_length=50, verbose_name='Cidade')),
                ('neighborhood', models.CharField(blank=True, default='', max_length=100, verbose_name='Bairro')),
                ('street', models.CharField(blank=True, default='', max_length=50, verbose_name='Rua')),
                ('block', models.CharField(blank=True, default='', max_length=50, verbose_name='Conjunto')),
                ('number', models.CharField(blank=True, default='', max_length=10, verbose_name='Numero')),
                ('date', models.DateField(auto_now=True, verbose_name='Data')),
                ('classification', models.IntegerField(choices=[(0, 'Não classificado'), (1, 'Atendimento Imediato'), (2, 'Atendimento Hospitalar'), (3, 'Atendimento Ambulatorial'), (4, 'Atendimento Eletivo')], default=0, verbose_name='Classification')),
                ('gender', models.IntegerField(blank=True, choices=[(0, 'Sexo indefinido'), (1, 'Feminino'), (2, 'Masculino')], default=0, verbose_name='Genero')),
                ('age_range', models.IntegerField(choices=[(0, 'Faixa etária indefinida'), (1, '0 até 28 dias'), (2, '29 dias à 2 meses'), (3, '2 meses à 3 anos'), (4, '3 anos à 10 anos'), (5, 'Acima de 10 anos')], default=0, verbose_name='Faixa etária')),
            ],
        ),
    ]
