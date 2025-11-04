from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
import json
from django.contrib.auth.models import User
from accounts.models import User
from rest_framework.views import APIView
from .permissions import IsParentOrStudent
from performance.models import Mark, Exam
from django.db.models import Q, Count
from datetime import datetime


from .models import Student, ParentStudent, Attendance, Standard, Section, Subject
from .serializers import (
    StudentRegistrationSerializer,
    LinkParentSerializer,
    AttendanceSerializer,
    AttendanceMarkSerializer,
    AttendanceSummarySerializer,
    StandardSerializer,
    SectionSerializer,
    SubjectSerializer,
    MarkSerializer,
    ExamSerializer,


)

class StudentMarksListView(generics.ListAPIView):
    serializer_class = MarkSerializer
    permission_classes = []
    queryset = Mark.objects.select_related('subject', 'exam', 'recorded_by','student')


    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, pk=student_id)

        # Check permissions
        self.check_object_permissions(self.request, student)
        qs = Mark.objects.filter(student=student)

        if exam_id:
            qs = qs.filter(exam_id=exam_id)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)

        return qs.order_by('-exam__date', 'subject__name')

class MyMarksListView(generics.ListAPIView):
    serializer_class = MarkSerializer
    permission_classes = []
    queryset = Mark.objects.select_related('subject', 'exam', 'recorded_by','student')

    def get_queryset(self):
        user = self.request.user
        student=getattr(user,'student_profile',None)
        if student:
            return self.queryset.filter(student=student).order_by('-exam__date', 'subject__name')

        from .models import ParentStudent
        children_ids = ParentStudent.objects.filter(parent=user).values_list('student_id', flat=True)
        student_id=self.request.query_params.get('student')
        if student_id and int(student_id) in set(children_ids):
            return self.queryset.filter(student_id=student_id).order_by('-exam__date', 'subject__name')
        
        return Mark.objects.none()

# -------------------------------
# Custom permission for teacher
# -------------------------------
class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


# -------------------------------
# Student registration
# -------------------------------
class StudentRegistrationView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    authentication_classes = [SessionAuthentication]


# -------------------------------
# Link Parent
# -------------------------------
class LinkParentView(generics.CreateAPIView):
    queryset = ParentStudent.objects.all()
    serializer_class = LinkParentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    authentication_classes = [SessionAuthentication]


# -------------------------------
# Standards
# -------------------------------
class StandardListCreateView(generics.ListCreateAPIView):
    queryset = Standard.objects.all()
    serializer_class = StandardSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


# -------------------------------
# Sections
# -------------------------------
class SectionListCreateView(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

from rest_framework.generics import ListCreateAPIView
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceView(ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer



# -------------------------------
# Mark attendance
# -------------------------------
class AttendanceMarkView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceMarkSerializer
    permission_classes = []  # you can add IsAuthenticated later

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            many = isinstance(data, list)
            serializer = self.get_serializer(data=data, many=many)
            serializer.is_valid(raise_exception=True)

            validated_data = serializer.validated_data if many else [serializer.validated_data]
            records = []
            teacher = User.objects.get(id=4)  # or use request.user later

            for item in validated_data:
                student_id = int(item['student_id'])
                date = item['date']
                status_value = item['status']

                attendance, created = Attendance.objects.update_or_create(
                    student_id=student_id,
                    date=date,
                    defaults={'status': status_value, 'marked_by': teacher}
                )
                records.append(attendance)

            return Response(
                AttendanceSerializer(records, many=True).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("Error:", e)
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AttendanceView(APIView):
    """
    GET: Retrieve all attendance
    POST: Mark attendance
    """

    def get(self, request):
        attendances = Attendance.objects.all().order_by('date')
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        if isinstance(data, dict):
            data = [data]  # wrap single object in a list
        serializer = AttendanceSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        for att_data in serializer.validated_data:
            Attendance.objects.create(
                student=att_data['student'],
                date=att_data['date'],
                status=att_data['status'],
                marked_by=request.user
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

                    



# -------------------------------
# Student’s attendance list
# -------------------------------
class StudentAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        if self.request.user.role == 'student' and self.request.user.id != int(student_id):
            return Attendance.objects.none()
        return Attendance.objects.filter(student_id=student_id).order_by('-date')


# -------------------------------
# Class attendance view
# -------------------------------
class ClassAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        section_id = self.kwargs['section_id']
        date = self.request.query_params.get('date')
        students = Student.objects.filter(section_id=section_id).values_list('id', flat=True)

        qs = Attendance.objects.filter(student_id__in=students)
        if date:
            qs = qs.filter(date=date)
        return qs.order_by('-date')


# -------------------------------
# Utility function
# -------------------------------
def calculate_attendance_percentage(present, total_days):
    if total_days == 0:
        return "0%"
    return f"{(present / total_days) * 100:.2f}%"


# -------------------------------
# Principal report view
# -------------------------------
class AttendanceReportPrincipalView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()  # principal sees all

        records = []
        total_students = students.count()
        total_days = Attendance.objects.values('date').distinct().count()

        overall_present = 0

        for student in students:
            total_present = Attendance.objects.filter(student=student, status='present').count()
            total_absent = Attendance.objects.filter(student=student, status='absent').count()

            overall_present += total_present

            records.append({
                "student_name": student.user.get_full_name() or student.user.username,
                "standard": student.standard.name if student.standard else "",
                "section": student.section.name if student.section else "",
                "total_present": total_present,
                "total_absent": total_absent,
                "attendance_percentage": calculate_attendance_percentage(total_present, total_days),
            })

        summary = {
            "total_students": total_students,
            "total_days": total_days,
            "overall_attendance_percentage": calculate_attendance_percentage(
                overall_present, total_students * total_days if total_days else 0
            ),
        }

        return Response({
            "summary": summary,
            "records": records,
        })




class AttendanceReportParentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get all students linked to this parent
        students = Student.objects.filter(parent=request.user)

        if not students.exists():
            return Response({"error": "No student(s) linked to this parent"}, status=404)

        records = []
        total_students = students.count()
        overall_present = 0

        for student in students:
            total_present = Attendance.objects.filter(student=student, status='present').count()
            total_absent = Attendance.objects.filter(student=student, status='absent').count()

            overall_present += total_present

            records.append({
                "student_name": student.user.get_full_name() or student.user.username,
                "standard": student.standard.name if student.standard else "",
                "section": student.section.name if student.section else "",
                "total_present": total_present,
                "total_absent": total_absent,
                "attendance_percentage": calculate_attendance_percentage(total_present, total_present + total_absent),
            })

        summary = {
            "total_students": total_students,
            "total_days": max(total_present + total_absent, 1),  # avoid division by zero
            "overall_attendance_percentage": calculate_attendance_percentage(
                overall_present, sum([r['total_present'] + r['total_absent'] for r in records])
            ),
        }

        return Response({
            "summary": summary,
            "records": records,
        })

