from django.urls import path
from .views import StudentRegistrationView, LinkParentView
urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='student-register'),
    path('link-parent/', LinkParentView.as_view(), name='link-parent'),

]
