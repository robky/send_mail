# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-02-18 06:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_auto_20230218_0837'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True)),
                ('was_read', models.DateTimeField(blank=True, null=True, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043f\u0440\u043e\u0447\u0442\u0435\u043d\u0438\u044f')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info', to='mailing.Mailing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info', to='mailing.User')),
            ],
        ),
    ]
