from rest_framework import serializers
from django.utils import timezone
from .models import Assignment, AssignmentSubmission



# ============================================================
# 📌 Assignment Serializer
# ============================================================
class AssignmentSerializer(serializers.ModelSerializer):
    assigned_by_name = serializers.CharField(source='assigned_by.get_full_name', read_only=True)

    class Meta:
        model = Assignment
        fields = [
            'id',
            'title',
            'description',      # fixed from 'descriptions'
            'subject_name',
            'assigned_by',
            'assigned_by_name',
            'file',
            'due_date',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'assigned_by']

    def create(self, validated_data):
        """
        Automatically assign the current user as the one who created the assignment.
        """
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)


# ============================================================
# 📌 Assignment Submission Serializer
# ============================================================
class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            'id',
            'assignment',
            'assignment_title',
            'student',
            'student_name',
            'file',           # matches your model
            'submitted_at',
            'remarks',
            'grade'
        ]
        read_only_fields = ['id', 'submitted_at', 'student_name', 'assignment_title']

    def validate(self, attrs):
        """
        Ensure student cannot submit multiple times and submission is before due date
        """
        assignment = attrs.get('assignment')
        student = self.context['request'].user

        today = timezone.now().date()
        if assignment.due_date.date() < today:
            raise serializers.ValidationError("Cannot submit assignment after the due date.")

        if AssignmentSubmission.objects.filter(assignment=assignment, student=student).exists():
            raise serializers.ValidationError("You have already submitted this assignment.")

        return attrs

    def create(self, validated_data):
        """Automatically assign the current user as the student"""
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)
