from rest_framework import serializers
from accounts.models import User
from .models import Student, Standard, Section, ParentStudent, Attendance, Subject
from performance.models import Mark,Exam


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code']

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'date', 'total_marks']

class MarkSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    exam = ExamSerializer(read_only=True)
    recorded_by = serializers.StringRelatedField()

    class Meta:
        model = Mark
        fields = ['id','student', 'subject', 'exam', 'marks_obtained', 'max_marks', 'grade', 'remarks', 'recorded_by', 'updated_at']
        read_only_fields = ['recorded_by', 'updated_at']
        



# -------------------------------
# Student Registration Serializer
# -------------------------------
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
        # extract nested user data
        user_data = validated_data.pop('user')
        standard_id = validated_data.pop('standard_id')
        section_id = validated_data.pop('section_id')

        # create user
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role='student'
        )

        # validate standard and section IDs
        try:
            standard = Standard.objects.get(id=standard_id)
        except Standard.DoesNotExist:
            raise serializers.ValidationError({"standard_id": "Invalid standard ID"})

        try:
            section = Section.objects.get(id=section_id)
        except Section.DoesNotExist:
            raise serializers.ValidationError({"section_id": "Invalid section ID"})

        # create student object
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


# -------------------------------
# Link Parent Serializer
# -------------------------------
class LinkParentSerializer(serializers.Serializer):
    parent_id = serializers.IntegerField()
    student_id = serializers.IntegerField()

    def validate(self, data):
        parent_id = data['parent_id']
        student_id = data['student_id']

        try:
            parent = User.objects.get(id=parent_id, role='parent')
        except User.DoesNotExist:
            raise serializers.ValidationError({"parent_id": "Parent with given ID does not exist or is not a parent."})

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
        link, created = ParentStudent.objects.get_or_create(
            parent=parent,
            student=student
        )
        return link

    def to_representation(self, instance):
        return {
            "link_id": instance.id,
            "parent_id": instance.parent.id,
            "student_id": instance.student.id
        }


# -------------------------------
# Section + Standard Serializers
# -------------------------------
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name', 'standard']


class StandardSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Standard
        fields = ['id', 'name', 'sections']


# -------------------------------
# Attendance Serializers
# -------------------------------
class AttendanceSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student'
    )

    class Meta:
        model = Attendance
        fields = ['student_id', 'date', 'status'] 


class AttendanceDailySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(read_only=True)
    standard = serializers.CharField(read_only=True)
    section = serializers.CharField(read_only=True)

    class Meta:
        model = Attendance
        fields = ['date', 'status', 'student_name', 'standard', 'section']


class AttendanceSummarySerializer(serializers.Serializer):
    student_name = serializers.CharField()
    standard = serializers.CharField()
    section = serializers.CharField()
    total_present = serializers.IntegerField()
    total_absent = serializers.IntegerField()
    attendance_percentage = serializers.CharField()


# This serializer is used to mark attendance
class AttendanceMarkSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Attendance
        fields = ['student_id', 'date', 'status']

    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        return Attendance.objects.create(student_id=student_id, **validated_data)






