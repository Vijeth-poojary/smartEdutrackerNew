from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.db.models import Sum, Avg

from Student.models import Student
from performance.models import Mark


# ---------------------- REPORT CARD (PDF GENERATION) ----------------------
class ReportCardView(APIView):
    permission_classes = []

    def get(self, request, student_id):
        # ✅ Get student or 404 if not found
        student = get_object_or_404(Student, id=student_id)

        # ✅ Get all marks for that student
        marks = Mark.objects.filter(student=student)

        if not marks.exists():
            return Response({"error": "No marks found for this student."}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Prepare PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_card_{student_id}.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(180, 820, "STUDENT REPORT CARD")

        # Student info
        p.setFont("Helvetica", 12)
        p.drawString(100, 780, f"Name: {student.user.first_name} {student.user.last_name}")
        if hasattr(student, 'standard') and student.standard:
            p.drawString(100, 760, f"Class: {student.standard.name}")
        else:
            p.drawString(100, 760, "Class: Not Assigned")

        # Table header
        y = 730
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Subject")
        p.drawString(250, y, "Exam")
        p.drawString(400, y, "Marks")
        y -= 20
        p.line(90, y + 10, 520, y + 10)

        # Table data
        p.setFont("Helvetica", 12)
        for mark in marks:
            p.drawString(100, y, str(mark.subject))
            p.drawString(250, y, str(mark.exam.name))
            p.drawString(400, y, f"{mark.marks_obtained}/{mark.max_marks}")
            y -= 20
            if y < 100:  # new page if space runs out
                p.showPage()
                y = 800

        # Totals
        totals = marks.aggregate(total_obtained=Sum('marks_obtained'), total_max=Sum('max_marks'))
        total_obtained = totals['total_obtained'] or 0
        total_max = totals['total_max'] or 0
        percentage = (total_obtained / total_max) * 100 if total_max > 0 else 0

        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y - 10, f"Total Marks: {total_obtained}/{total_max}")
        p.drawString(100, y - 30, f"Percentage: {round(percentage, 2)}%")

        # Finalize PDF
        p.showPage()
        p.save()
        return response


# ---------------------- CLASS PERFORMANCE (AVERAGE MARKS) ----------------------
class ClassPerformanceView(generics.ListAPIView):
    permission_classes = []

    def list(self, request):
        data = (
            Mark.objects.values('student__standard__name')
            .annotate(average_marks=Avg('marks_obtained'))
            .order_by('student__standard__name')
        )
        return Response(data)


# ---------------------- TOP 3 PERFORMERS ----------------------
class TopPerformersView(generics.ListAPIView):
    permission_classes = []

    def list(self, request):
        top_performers = (
            Mark.objects.values(
                'student__id',
                'student__user__first_name',
                'student__user__last_name',
                'student__standard__name',
            )
            .annotate(total_marks=Sum('marks_obtained'))
            .order_by('-total_marks')[:3]
        )
        return Response(top_performers)
