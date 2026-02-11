from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3}, countdown=5)
def send_verification_email(self, subject, message, recipient):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)