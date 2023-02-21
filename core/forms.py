# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from mailing import models


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = '__all__'


class CreateMailingForm(forms.ModelForm):
    class Meta:
        model = models.Mailing
        fields = '__all__'


class SendMailForm(forms.Form):
    countdown = forms.IntegerField(
        label="Отсрочка отправки, секунды",
        help_text=("Если требуется отсрочка отправки укажите время в секундах."
                   " Если не указано, то отправка без отсрочки."),
        min_value=0,
        widget=forms.TextInput(attrs={'placeholder': 0}),
        required=False
    )
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    eta = forms.DateTimeField(
        label="Дата и время отправки",
        help_text=("Отправка будет осуществлена не раньше указанного времени."
                   "Если не указано или указано время в прошлом, то отправка "
                   "текущим временем."),
        input_formats=['%d.%m.%Y %H:%M'],
        widget=forms.TextInput(attrs={'placeholder': now}),
        required=False
    )
