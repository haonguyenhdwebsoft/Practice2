from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task()
def notify_user(email):
    subject = "Notification"
    message = "You have created new product"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])