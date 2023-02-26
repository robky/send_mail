# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bootstrap_modal_forms import generic
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from core import forms, tasks
from mailing.models import Info, Journal, Mailing, Subscribe, User

ONE_PIXEL_DATA = """R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7
""".strip().decode('base64')


def index(request):
    template = 'core/index.html'
    title = 'Отправка почтовых сообщений'
    context = {
        'title': title,
    }
    return render(request, template, context)


def mailing_table(request):
    template = "core/mailing_table.html"
    title = "Рассылки"
    mailings = Mailing.objects.prefetch_related('subscribe')

    context = {
        'title': title,
        'mailings': mailings,
    }
    return render(request, template, context)


class MailingDetailView(generic.BSModalReadView):
    model = Mailing
    template_name = 'core/mailing_detail.html'
    success_url = reverse_lazy('core:mailing_table')


class MailingCreateView(generic.BSModalCreateView):
    template_name = 'core/mailing_create.html'
    form_class = forms.MailingModelForm
    success_message = 'Рассылка успешно создана.'
    success_url = reverse_lazy('core:mailing_table')


class MailingDeleteView(generic.BSModalDeleteView):
    model = Mailing
    template_name = 'core/mailing_delete.html'
    success_message = 'Рассылка удалена.'
    success_url = reverse_lazy('core:mailing_table')


class MailingUpdateView(generic.BSModalUpdateView):
    model = Mailing
    template_name = 'core/mailing_create.html'
    form_class = forms.MailingModelForm
    success_message = 'Рассылка успешно изменена.'
    success_url = reverse_lazy('core:mailing_table')

    def get_context_data(self, **kwargs):
        context = super(MailingUpdateView, self).get_context_data(**kwargs)
        context["is_edit"] = True
        return context


def mailing_subscribe(request, mailing_id):
    template = "core/mailing_subscribe.html"
    mailing = get_object_or_404(Mailing.objects, id=mailing_id)
    subscribe_users = mailing.subscribe.all()
    unsubscribe_users = User.objects.exclude(
        subscriber__in=subscribe_users)

    context = {
        "mailing_id": mailing_id,
        "unsubscribe_users": unsubscribe_users,
    }
    return render(request, template, context)


def mailing_subscribe_user(request, mailing_id, user_id):
    mailing = get_object_or_404(Mailing.objects, id=mailing_id)
    user = get_object_or_404(User, id=user_id)
    if not mailing.subscribe.filter(user=user).exists():
        Subscribe.objects.create(mailing=mailing, user=user)
    message = 'Пользователь {} успешно подписан на рассылку {}'.encode(
        'utf-8').format(user, mailing)
    messages.success(request, message)
    return redirect('/mailings/')


def mailing_unsubscribe_user(request, mailing_id, user_id):
    mailing = get_object_or_404(Mailing.objects, id=mailing_id)
    user = get_object_or_404(User, id=user_id)
    subscribe = get_object_or_404(Subscribe, mailing=mailing, user=user)
    subscribe.delete()
    message = 'Пользователь {} успешно отписан от рассылки {}'.encode(
        'utf-8').format(user, mailing)
    messages.success(request, message)
    return redirect('/mailings/')


def mailing_users(request, mailing_id):
    template = "core/mailing_users.html"
    mailing = get_object_or_404(Mailing.objects, id=mailing_id)
    subscribe = mailing.subscribe.all()

    context = {
        "mailing_id": mailing_id,
        "subscribe": subscribe,
    }
    return render(request, template, context)


def mailing_send_form(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)
    form = forms.SendMailForm(request.POST or None)
    if form.is_valid() and request.is_():
        countdown = form.cleaned_data['countdown']
        eta = form.cleaned_data['eta']
        url = request.build_absolute_uri(reverse('core:index'))
        tasks.preparing_mailing.delay(mailing_id, countdown, eta, url)
        messages.success(
            request,
            ('Задание на рассылку сформировано. Рассылка будет отправлена '
             'согласно указанным временным настройкам.')
        )
        message = 'Отслеживать рассылку можно в журнале отправленных рассылок'
        messages.info(request, message)
        return redirect('/mailings/')
    if form.is_valid():
        return redirect('/mailings/')
    template = 'core/mailing_send.html'
    context = {
        'form': form,
        'mailing_id': mailing.id,
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


class UserCreateView(generic.BSModalCreateView):
    template_name = 'core/user_create.html'
    form_class = forms.UserModelForm
    success_message = 'Пользователь успешно создан.'
    success_url = reverse_lazy('core:user_table')


class UserUpdateView(generic.BSModalUpdateView):
    model = User
    template_name = 'core/user_create.html'
    form_class = forms.UserModelForm
    success_message = 'Пользователь успешно изменен.'
    success_url = reverse_lazy('core:user_table')

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context["is_edit"] = True
        return context


class UserDetailView(generic.BSModalReadView):
    model = User
    template_name = 'core/user_detail.html'
    success_url = reverse_lazy('core:user_table')


class UserDeleteView(generic.BSModalDeleteView):
    model = User
    template_name = 'core/user_delete.html'
    success_message = 'Пользователь удален.'
    success_url = reverse_lazy('core:user_table')


def info_table(request):
    template = "core/info_table.html"
    title = "Журнал рассылок"
    info_stack = Info.objects.all()
    now_time = timezone.now()

    context = {
        'title': title,
        'info_stack': info_stack,
        'now_time': now_time,
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
