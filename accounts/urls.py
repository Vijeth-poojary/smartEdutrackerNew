from django.urls import path
from .views import (
    CreateParentTeacherView,
    SessionLoginView,
    SessionLogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView
)
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('accounts/create-parent-teacher/', CreateParentTeacherView.as_view(), name='create-parent-teacher'),
    path('accounts/login/', SessionLoginView.as_view(), name='session-login'),
    path('accounts/logout/', SessionLogoutView.as_view(), name='session-logout'),
    path('accounts/password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('accounts/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('gettoken/', csrf_exempt(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('refreshtoken/', csrf_exempt(TokenRefreshView.as_view()), name='token_refresh'),
    path('verifytoken/', csrf_exempt(TokenVerifyView.as_view()), name='token_verify'),

]
