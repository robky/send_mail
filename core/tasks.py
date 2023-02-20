from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from django.core.mail import send_mail
from django.forms import model_to_dict

from mailing.models import Mailing, Info, Journal
from send_mail import settings
from send_mail.celery import app
from uuid import uuid4
from django.template import Context, Template


@app.task
def add(x, y):
    return x + y


@app.task
def preparing_mailing(mailing_id, countdown, eta, url):
    deferred = False
    if eta or countdown:
        deferred = True

    mailing = Mailing.objects.get(id=mailing_id)
    subscribe_users = mailing.subscribe.all()
    if subscribe_users:
        info = Info.objects.create(mailing=mailing)
    for subscribe in subscribe_users:
        uuid_string = str(uuid4())
        Journal.objects.create(
            id=uuid_string,
            info=info,
            user=subscribe.user,
        )
        img_url = "{}info/{}/".format(url, uuid_string)
        img_track = '\n<img src="{}" height="1px" width="1px">'.format(img_url)
        template = Template(mailing.template + img_track)
        context = Context(model_to_dict(subscribe.user))
        rendered = template.render(context)

        if deferred:
            if eta:
                mailing_send.apply_async(
                    mailing.title, subscribe.user.mail, rendered,
                    eta=eta + timedelta(seconds=countdown)
                )
            else:
                mailing_send.apply_async(
                    mailing.title, subscribe.user.mail, rendered,
                    countdown=countdown
                )
        else:
            mailing_send.delay(mailing.title, subscribe.user.mail, rendered)


@app.task
def mailing_send(subject, recipient, message):
    return send_mail(
        subject=subject,
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient],
        html_message=message,
    )
