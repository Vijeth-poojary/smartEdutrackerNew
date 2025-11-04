from django.db import models
from django.conf import settings
from accounts.models import User


def assignment_upload_path(instance, filename):
    return f"assignments/{instance.subject_name}/{filename}"


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject_name = models.CharField(max_length=100, default="Unknown")
    assigned_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assignments_given"
    )
    file = models.FileField(upload_to=assignment_upload_path, blank=True, null=True)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.subject_name})"


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='submissions'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    file = models.FileField(upload_to='assignment_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"
