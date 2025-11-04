from django.db import models
from accounts.models import User   # your custom user
from Student.models import Student, Standard, Section, Attendance

# Create your models here.
class Exam(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='exams')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='exams')
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.standard.name} - {self.section.name}"

class Mark(models.Model):
    exam=models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks')
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject=models.CharField(max_length=100)
    marks_obtained=models.DecimalField(max_digits=5, decimal_places=2)
    max_marks=models.DecimalField(max_digits=5, decimal_places=2)
    remarks=models.TextField(blank=True, null=True)
    grade=models.CharField(max_length=2, blank=True, null=True)
    entered_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.max_marks and self.marks_obtained is not None:
            percentage = (self.marks_obtained / self.max_marks) * 100
            if percentage >= 90:
                self.grade = 'A+'
            elif percentage >= 75:
                self.grade = 'A'
            elif percentage >= 60:
                self.grade = 'B+'
            elif percentage >= 50:
                self.grade = 'B'
            elif percentage >= 45:
                self.grade = 'C'
            else:
                self.grade = 'D'
        super().save(*args, **kwargs)
