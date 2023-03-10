from __future__ import absolute_import, unicode_literals

from datetime import timedelta
from uuid import uuid4

from dateutil import parser
from django.core.mail import send_mail
from django.forms import model_to_dict
from django.template import Context, Template
from django.utils import timezone

from mailing.models import Info, Journal, Mailing
from send_mail import settings
from send_mail.celery import app


@app.task
def preparing_mailing(mailing_id, countdown, eta, url):
    time_now = timezone.now()
    time_planned = time_now
    if countdown is None:
        countdown = 0
    if eta:
        if isinstance(eta, unicode):
            eta = parser.parse(eta)
        if countdown:
            time_planned = eta + timedelta(seconds=countdown)
    else:
        time_planned = time_now + timedelta(seconds=countdown)

    mailing = Mailing.objects.get(id=mailing_id)
    subscribe_users = mailing.subscribe.all()
    if subscribe_users:
        info = Info.objects.create(
            mailing=mailing, created=time_now, time_planned_send=time_planned)

    for subscribe in subscribe_users:
        uuid_string = str(uuid4())
        Journal.objects.create(
            id=uuid_string,
            info=info,
            user=subscribe.user,
        )
        img_url = "{}info/{}.gif".format(url, uuid_string)
        img_track = '\n<img src="{}" height="1px" width="1px">'.format(img_url)
        template = Template(mailing.template + img_track)
        context = Context(model_to_dict(subscribe.user))
        rendered = template.render(context)

        if eta or countdown:
            mailing_send.apply_async(
                (mailing.title, subscribe.user.mail, rendered),
                eta=time_planned
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
