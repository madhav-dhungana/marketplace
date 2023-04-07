
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404
from celery import shared_task
from user.models import User


@shared_task
def background_email_send(title, message, send_to):
    try:
        email = EmailMessage(title, message, settings.EMAIL_HOST_USER, to=send_to)
        email.content_subtype = "html"
        email.fail_silently = False
        email.send()
    except Exception as e:
        pass


@shared_task
def read_user_unread_notification(id):
    user = get_object_or_404(User,id=id)
    user.notification_to.filter(user_has_seen=False).update(user_has_seen=True)
