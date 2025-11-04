from django.contrib import admin
from .models import Standard, Section, Student, ParentStudent

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


# Register your models here.



