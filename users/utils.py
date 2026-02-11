from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse 
from django.conf import settings
from .tokens import email_verification_token

def build_verification_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    
    return f"{settings.BACKEND_URL}/api/verify-email/{uid}/{token}/"
