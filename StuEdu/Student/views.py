from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .models import Student
from .serializers import StudentRegistrationSerializer
from .serializers import LinkParentSerializer


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return request.user.is_authenticated and request.user.role == 'teacher'


class StudentRegistrationView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    authentication_classes = [SessionAuthentication]

class LinkParentView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = LinkParentSerializer
    permission_classes = [IsTeacher]
    


   
