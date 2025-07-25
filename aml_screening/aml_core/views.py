
from rest_framework.decorators import api_view
from .utils.response import standard_response
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from rest_framework.permissions import AllowAny

from .serializers import (
    RegisterSerializer, CustomTokenObtainPairSerializer,
    PasswordResetSerializer, SetNewPasswordSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://localhost:4200/reset-password/{uid}/{token}/"
        send_mail(
            subject='Password Reset',
            message=f'Click to reset: {reset_link}',
            from_email=None,
            recipient_list=[email],
        )
        return Response({'detail': 'Password reset email sent.'})

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        data = request.data
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'error': 'Invalid link.'}, status=400)

        if not default_token_generator.check_token(user, data['token']):
            return Response({'error': 'Token expired or invalid.'}, status=400)

        user.set_password(data['new_password'])
        user.save()
        return Response({'detail': 'Password has been reset.'})

# Create your views here.
@api_view(['GET'])
def sample_view(request):
    data = {"message": "Welcome!"}
    # return standard_response(data=data, status_code=status.HTTP_200_OK)
    return Response("Welcome")
