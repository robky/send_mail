# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Mailing(models.Model):
    title = models.CharField(
        verbose_name="Название",
        help_text='Введите название рассылки',
        max_length=30
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text='Введите описание рассылки',
    )
    template = models.TextField(
        verbose_name="Шаблон",
        help_text=('Введите шаблон рассылки. Можно использовать html теги, и '
                   'поля пользователя заключенные в двойные фигурные скобки '
                   'например: {{name}} - имя, {{surname}} - фамилия, '
                   '{{birthday}} - день рождения)'),
    )

    def __str__(self):
        return self.title.encode('utf-8')


class User(models.Model):
    name = models.CharField(
        verbose_name="Имя",
        help_text="Введите имя пользователя",
        max_length=15
    )
    surname = models.CharField(
        verbose_name="Фамилия",
        help_text="Введите фамилию пользователя",
        max_length=30)
    mail = models.EmailField(
        verbose_name="Электронная почта",
        help_text="Введите электронную почту пользователя",
    )
    birthday = models.DateField(
        verbose_name="День рождения",
        help_text="Введите дату рождения пользователя",
    )

    def __str__(self):
        return "{} {} ({})".format(
            self.name, self.surname, self.mail).encode('utf-8')


class Subscribe(models.Model):
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='subscribe'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )


class Info(models.Model):
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='info'
    )
    created = models.DateTimeField(auto_now_add=True)


class Journal(models.Model):
    id = models.CharField(primary_key=True, max_length=36, unique=True)
    info = models.ForeignKey(
        Info,
        on_delete=models.CASCADE,
        related_name='journal'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='journal'
    )
    was_read = models.DateTimeField("Время прочтения", blank=True, null=True)
