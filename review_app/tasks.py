from __future__ import absolute_import

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def contact_email(name, from_email, user, form_message, subject):
    message = "{} / {} / {} said: \n\n{}".format(name, from_email, user, form_message)
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=['fathen.co@gmail.com'],
    )
