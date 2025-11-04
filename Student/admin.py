from django.contrib import admin
from .models import Standard, Section, Student, ParentStudent, Attendance

@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'standard')
    list_filter = ('standard',)
    search_fields = ('name', 'standard__name')
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'standard', 'section', 'created_at')
    list_filter = ('standard', 'section')
    search_fields = ('user__username', 'standard__name', 'section__name')

@admin.register(ParentStudent)
class ParentStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'student')
    search_fields = ('parent__username', 'student__user__username')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'date', 'status', 'marked_by')
    list_filter = ('date', 'status', 'marked_by')
    search_fields = ('student__username', 'marked_by__username')
    


# Register your models here.



