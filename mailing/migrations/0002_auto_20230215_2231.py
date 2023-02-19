# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-02-15 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='template',
            field=models.TextField(default=1, verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mailing',
            name='description',
            field=models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='title',
            field=models.CharField(max_length=30, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='user',
            name='mail',
            field=models.EmailField(max_length=254, verbose_name='\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u043f\u043e\u0447\u0442\u0430'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=15, verbose_name='\u0418\u043c\u044f'),
        ),
        migrations.AlterField(
            model_name='user',
            name='surname',
            field=models.CharField(max_length=30, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f'),
        ),
    ]
