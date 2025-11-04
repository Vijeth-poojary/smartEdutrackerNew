from django.urls import path
from .views import CreateParentTeacherView

urlpatterns = [
    path('create-parent-teacher/', CreateParentTeacherView.as_view(), name='create-parent-teacher'),
]
