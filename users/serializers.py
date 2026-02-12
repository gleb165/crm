# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .tasks import send_verification_email
from .utils import build_verification_link

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,
        )

        link = build_verification_link(user)

        send_verification_email.delay(
            subject='Verify your email',
            message=f'Click to verify:\n{link}',
            recipient=user.email
        )

        return user

# this serializer is give user to resend verification email
class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self, **kwargs):
        email = self.validated_data["email"].lower().strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            
            return

        if user.is_active:
            return

        link = build_verification_link(user)
        send_verification_email.delay(
            subject="Verify your email",
            message=f"Click to verify:\n{link}",
            recipient=user.email
        )

