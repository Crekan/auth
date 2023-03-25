from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from users.models import CustomUser
from .serializers import CustomUserRegisterSerializer, CustomUserLoginSerializer, PasswordResetSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = CustomUserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'})


class PasswordReset(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(username=user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        response = auth_views.PasswordResetView.as_view(
            extra_email_context={'email': email}
        )(request._request)
        if response.status_code == 302:
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        else:
            return response
