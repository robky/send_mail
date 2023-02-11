# -*- coding: utf-8 -*-
from django import forms


class TwoNumbersForm(forms.Form):
    one = forms.IntegerField(label="Первое число")
    two = forms.IntegerField(label="Второе число")