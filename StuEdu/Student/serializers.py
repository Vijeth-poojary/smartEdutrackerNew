from rest_framework import serializers
from accounts.models import User
from .models import Student, Standard, Section, ParentStudent  # Make sure ParentStudent is from the correct app


# --------------------------
# Student Registration
# --------------------------
class StudentRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True, source='user.password')
    standard_id = serializers.IntegerField(write_only=True)
    section_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'password', 'standard_id', 'section_id']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        standard_id = validated_data.pop('standard_id')
        section_id = validated_data.pop('section_id')

        # Create user with hashed password automatically
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role='student'
        )

        # Validate standard and section IDs
        try:
            standard = Standard.objects.get(id=standard_id)
        except Standard.DoesNotExist:
            raise serializers.ValidationError({"standard_id": "Invalid standard ID"})

        try:
            section = Section.objects.get(id=section_id)
        except Section.DoesNotExist:
            raise serializers.ValidationError({"section_id": "Invalid section ID"})

        # Create the student
        student = Student.objects.create(
            user=user,
            standard=standard,
            section=section
        )
        return student

    def to_representation(self, instance):
        return {
            "student_id": instance.id,
            "name": instance.user.get_full_name() or instance.user.username,
            "email": instance.user.email,
            "standard": instance.standard.name if instance.standard else None,
            "section": instance.section.name if instance.section else None,
            "created_at": instance.created_at
        }


# --------------------------
# Link Parent to Student
# --------------------------
class LinkParentSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(write_only=True)
    student_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ParentStudent
        fields = ['id', 'parent_id', 'student_id']

    def validate(self, data):
        parent_id = data.get('parent_id')
        student_id = data.get('student_id')

        # Validate Parent
        try:
            parent = User.objects.get(id=parent_id, role='parent')
        except User.DoesNotExist:
            raise serializers.ValidationError({"parent_id": "Parent with given ID does not exist or is not a parent."})

        # Validate Student
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise serializers.ValidationError({"student_id": "Student with given ID does not exist."})

        data['parent'] = parent
        data['student'] = student
        return data

    def create(self, validated_data):
        parent = validated_data['parent']
        student = validated_data['student']

        parent_student_link, created = ParentStudent.objects.get_or_create(
            parent=parent,
            student=student
        )
        return parent_student_link
    def to_representation(self, instance):
        return {
            "Link ID": instance.id,
            "Student": instance.student.user.get_full_name() or instance.student.user.username,
            "Parent": instance.parent.get_full_name() or instance.parent.username,  
            "message": "Parent linked to student successfully."
        }
        
        