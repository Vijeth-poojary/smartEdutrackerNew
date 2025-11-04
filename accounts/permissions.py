from rest_framework.permissions import BasePermission

class IsTeacherOrPrincipal(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role in ['teacher','principal']

# Only teachers and principals can enter marks and create exams

class IsPrincipal(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role in ['principal']

# Only principals can create users and assign roles

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role in ['student']
        
# Only students can view their own assignments and marks





