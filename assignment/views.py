from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .models import Assignment, AssignmentSubmission
from .serializers import AssignmentSerializer, AssignmentSubmissionSerializer
from accounts.permissions import IsTeacherOrPrincipal, IsStudent


class AssignmentSubmissionCreateView(generics.CreateAPIView):
    """
    POST /api/assignments/submit/
    --------------------------------
    Allows students to submit their assignment submissions.
    """
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]





class AssignmentCreateView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


class AssignmentListView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = super().get_queryset()
        subject_id = self.request.query_params.get('subject')
        teacher_id = self.request.query_params.get('teacher')

        if subject_id:
            queryset = queryset.filter(subject_name__icontains=subject_id)
        if teacher_id:
            queryset = queryset.filter(assigned_by_id=teacher_id)

        return queryset


