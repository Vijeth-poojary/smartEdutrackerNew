from django.urls import path
from .views import (
    StudentRegistrationView,
    LinkParentView,
    StandardListCreateView,
    SectionListCreateView,
    AttendanceMarkView,
    StudentAttendanceView,
    ClassAttendanceView,
    AttendanceReportPrincipalView,
    AttendanceReportParentView,
    AttendanceView,
    StudentMarksListView,
    MyMarksListView,
)

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='student-register'),
    path('link-parent/', LinkParentView.as_view(), name='link-parent'),
    path('standards/', StandardListCreateView.as_view(), name='standard-list-create'),
    path('sections/', SectionListCreateView.as_view(), name='section-list-create'),
    path('students/attendance/', AttendanceView.as_view(), name='attendance'),
    path('mark-attendance/', AttendanceMarkView.as_view(), name='mark-attendance'),
    path('student-attendance/<int:student_id>/', StudentAttendanceView.as_view(), name='student-attendance'),
    path('class-attendance/<int:section_id>/', ClassAttendanceView.as_view(), name='class-attendance'),
    path('attendance-report/principal/', AttendanceReportPrincipalView.as_view(), name='attendance-report-principal'),
    path("attendance-report/parent/", AttendanceReportParentView.as_view(), name="attendance-report-parent"),
    path('students/<int:student_id>/marks/', StudentMarksListView.as_view(), name='student-marks'),
    path('students/me/marks/', MyMarksListView.as_view(), name='my-marks'),




  



]
