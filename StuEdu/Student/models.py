from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.models import User


class Standard(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=5)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return f"{self.standard.name} - {self.name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    standard = models.ForeignKey(Standard, on_delete=models.SET_NULL, null=True, related_name='students')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def __str__(self):
        return self.user.get_full_name() 

    

class ParentStudent(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name='parents')

   

    def __str__(self):
        return f"{self.parent.get_full_name()} - {self.student.user.get_full_name()}"
   