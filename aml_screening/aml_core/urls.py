from django.urls import path
from .views import sample_view  # Replace with your actual views
from django.urls import path
from .views import (
    RegisterView, CustomTokenObtainPairView, TokenRefreshView,
    PasswordResetView, PasswordResetConfirmView
)

urlpatterns = [
    path('screen/', sample_view),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]