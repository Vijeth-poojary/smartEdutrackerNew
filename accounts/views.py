from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from .models import User
from .serializers import (
    CreateUserSerializer,
    SessionLoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)

# --------------------------
# Create Parent/Teacher
# --------------------------
class CreateParentTeacherView(CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    # If only logged-in admin can create:
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    # If public sign-up allowed, change above to:
    # permission_classes = [AllowAny]

# --------------------------
# Session Login
# --------------------------
class SessionLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SessionLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                "message": "Login Successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --------------------------
# Session Logout
# --------------------------
class SessionLogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout Successful"}, status=status.HTTP_200_OK)

# --------------------------
# Password Reset Request
# --------------------------
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = f"http://example.com/reset-password-confirm/?uid={uid}&token={token}"



                # In production send email here.
                return Response({
                    "message": "Password reset link has been generated.",
                    "reset_link_for_testing": reset_link
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "No user is associated with this username."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --------------------------
# Password Reset Confirm
# --------------------------
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
