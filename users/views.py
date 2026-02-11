# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from .tokens import email_verification_token

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'detail': 'Check your email to verify account'},
            status=status.HTTP_201_CREATED
        )


User = get_user_model()

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Email verified successfully")

    return HttpResponse("Invalid or expired link", status=400)
