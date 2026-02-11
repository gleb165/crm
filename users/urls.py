# users/urls.py
from django.urls import path
from .views import RegisterAPIView, verify_email

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('verify-email/<uidb64>/<token>/', verify_email),
]
