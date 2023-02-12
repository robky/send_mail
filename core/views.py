# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from core import tasks
from core.forms import TwoNumbersForm


def index(request):
    template = 'core/index.html'
    title = 'Отправка почтовых сообщений'
    context = {
        'title': title,
    }
    return render(request, template, context)


def add(request):
    if request.method == 'POST':
        form = TwoNumbersForm(request.POST)
        if form.is_valid():
            one = form.cleaned_data['one']
            two = form.cleaned_data['two']
            tasks.add.delay(one, two)
            return HttpResponseRedirect('/done/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TwoNumbersForm()

    template = 'core/add.html'
    title = 'Сложение двух чисел'
    context = {
        'title': title,
        'form': form,
    }

    return render(request, template, context)


def done(request):
    template = 'core/done.html'
    title = 'Успешное выполнение задания'
    context = {
        'title': title,
    }
    return render(request, template, context)


def add_eta(request):
    if request.method == 'POST':
        form = TwoNumbersForm(request.POST)
        if form.is_valid():
            one = form.cleaned_data['one']
            two = form.cleaned_data['two']
            tasks.add.delay((one, two), countdown=0.2 * 60)
            return HttpResponseRedirect('/done/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TwoNumbersForm()

    template = 'core/add.html'
    title = 'Отложенное сложение двух чисел'
    context = {
        'title': title,
        'form': form,
    }

    return render(request, template, context)
