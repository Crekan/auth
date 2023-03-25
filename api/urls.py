from django.urls import path

from api.views import RegisterView, LoginView, PasswordReset

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password/reset/', PasswordReset.as_view(), name='password_reset'),
]