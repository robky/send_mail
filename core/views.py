# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from uuid import uuid4

from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.template.loader import get_template, render_to_string
from django.urls import reverse

from core import tasks, forms
from core.tasks import mailing_send
from mailing.models import Mailing, User, Subscribe, Info, Journal
from django.utils import timezone

LIMIT_COUNT_PAGINATOR = 7
ONE_PIXEL_DATA = """R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
""".strip().decode('base64')


def index(request):
    template = 'core/index.html'
    title = 'Отправка почтовых сообщений'
    title = str(uuid4())
    context = {
        'title': title,
    }
    return render(request, template, context)


def mailing_table(request):
    template = "core/mailing_table.html"
    title = "Рассылки"
    mailings = Mailing.objects.all()

    context = {
        'title': title,
        'mailings': mailings,
    }
    return render(request, template, context)


def mailing_detail(request, mailing_id):
    template = "core/mailing_detail.html"
    title = "Рассылка"
    mailing = get_object_or_404(Mailing.objects, id=mailing_id)

    context = {
        "title": title,
        "mailing": mailing,
    }
    return render(request, template, context)


def mailing_create(request):
    form = forms.CreateMailingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/mailings/')
    template = 'core/mailing_create.html'
    title = 'Добавить рассылку'
    context = {
        'title': title,
        'form': form,
    }
    return render(request, template, context)


def mailing_delete(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)
    mailing.delete()
    return redirect('/mailings/')


def mailing_edit(request, mailing_id):
    template = 'core/mailing_create.html'
    mailing = get_object_or_404(Mailing, id=mailing_id)
    form = forms.CreateMailingForm(
        request.POST or None,
        instance=mailing
    )
    if form.is_valid():
        form.save()
        return redirect('/mailings/')
    context = {
        'form': form,
        'is_edit': True,
        'mailing_id': mailing_id,
    }
    return render(request, template, context)


def mailing_subscribe(request, mailing_id):
    template = "core/mailing_subscribe.html"
    title = "Добавить подписчика в рассылку"
    mailing = get_object_or_404(Mailing.objects, id=mailing_id)
    subscribe_users = mailing.subscribe.all()
    unsubscribe_users = User.objects.exclude(id__in=subscribe_users)

    context = {
        "title": title,
        "mailing_id": mailing_id,
        "unsubscribe_users": unsubscribe_users,
    }
    return render(request, template, context)


def mailing_subscribe_user(request, mailing_id, user_id):
    mailing = get_object_or_404(Mailing.objects, id=mailing_id)
    user = get_object_or_404(User, id=user_id)
    if not mailing.subscribe.filter(user=user).exists():
        Subscribe.objects.create(mailing=mailing, user=user)
    return redirect('/mailings/{}/users/'.format(mailing_id))


def mailing_unsubscribe_user(request, mailing_id, user_id):
    mailing = get_object_or_404(Mailing.objects, id=mailing_id)
    user = get_object_or_404(User, id=user_id)
    subscribe = get_object_or_404(Subscribe, mailing=mailing, user=user)
    subscribe.delete()
    return redirect('/mailings/{}/users/'.format(mailing_id))


def mailing_users(request, mailing_id):
    template = "core/mailing_users.html"
    title = "Управление пользователями в рассылке"
    mailing = get_object_or_404(Mailing.objects, id=mailing_id)
    subscribe = mailing.subscribe.all()

    context = {
        "title": title,
        "mailing_id": mailing_id,
        "subscribe": subscribe,
    }
    return render(request, template, context)


def mailing_send_form(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)
    form = forms.SendMailForm(request.POST or None)
    if form.is_valid():
        countdown = form.cleaned_data['countdown']
        eta = form.cleaned_data['eta']
        url = request.build_absolute_uri(reverse('core:index'))
        tasks.preparing_mailing(mailing_id, countdown, eta, url)
        return redirect('/done/')
    template = 'core/mailing_send.html'
    title = 'Планирование отправки рассылки'
    context = {
        'title': title,
        'form': form,
        'mailing_id': mailing_id,
    }
    return render(request, template, context)


def user_table(request):
    template = "core/user_table.html"
    title = "Пользователи"
    users = User.objects.all()

    context = {
        'title': title,
        'users': users,
    }
    return render(request, template, context)


def user_detail(request, user_id):
    template = "core/user_detail.html"
    title = "Пользователь"
    user = get_object_or_404(User.objects, id=user_id)

    context = {
        "title": title,
        "user": user,
    }
    return render(request, template, context)


def user_create(request):
    form = forms.CreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/users/')
    template = 'core/user_create.html'
    title = 'Добавить пользователя'
    context = {
        'title': title,
        'form': form,
    }
    return render(request, template, context)


def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('/users/')


def user_edit(request, user_id):
    template = 'core/user_create.html'
    user = get_object_or_404(User, id=user_id)
    form = forms.CreateUserForm(
        request.POST or None,
        instance=user
    )
    if form.is_valid():
        form.save()
        return redirect('/users/')
    context = {
        'form': form,
        'is_edit': True,
        'user_id': user_id,
    }
    return render(request, template, context)


def info_table(request):
    template = "core/info_table.html"
    title = "Журнал рассылок"
    info_stack = Info.objects.all()

    context = {
        'title': title,
        'info_stack': info_stack,
    }
    return render(request, template, context)


def journal_table(request, info_id):
    info = get_object_or_404(Info, id=info_id)
    template = "core/journal_table.html"
    title = "Отслеживание открытий писем"
    journal_stack = info.journal.all()

    context = {
        'title': title,
        'journal_stack': journal_stack,
    }
    return render(request, template, context)


def done(request):
    template = 'core/done.html'
    title = 'Задание отправлено на выполнение'
    context = {
        'title': title,
    }
    return render(request, template, context)


def info(request, uuid_string):
    journal = get_object_or_404(Journal, id=uuid_string)
    journal.was_read = timezone.now()
    journal.save()
    return HttpResponse(ONE_PIXEL_DATA, content_type='image/gif')


def add(request):
    if request.method == 'POST':
        form = forms.TwoNumbersForm(request.POST)
        if form.is_valid():
            one = form.cleaned_data['one']
            two = form.cleaned_data['two']
            tasks.add.delay(one, two)
            return HttpResponseRedirect('/done/')

    else:
        form = forms.TwoNumbersForm()

    template = 'core/add.html'
    title = 'Сложение двух чисел'
    context = {
        'title': title,
        'form': form,
    }
    return render(request, template, context)


def add_eta(request):
    if request.method == 'POST':
        form = forms.TwoNumbersForm(request.POST)
        if form.is_valid():
            one = form.cleaned_data['one']
            two = form.cleaned_data['two']
            tasks.add.apply_async((one, two), countdown=0.2 * 60)
            return HttpResponseRedirect('/done/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.TwoNumbersForm()

    template = 'core/add_eta.html'
    title = 'Отложенное сложение двух чисел'
    context = {
        'title': title,
        'form': form,
    }

    return render(request, template, context)
