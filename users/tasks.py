from celery import shared_task
import sentry_sdk
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3}, countdown=5)
def send_verification_email(self, subject, message, recipient):
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        
    except Exception as e:
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("email_type", "verification")
            scope.set_extra("recipient", recipient)
        sentry_sdk.capture_exception(e)
        raise