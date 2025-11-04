from django.urls import path
from .views import AssignmentCreateView , AssignmentListView , AssignmentSubmissionCreateView

urlpatterns = [
    path("assignments/", AssignmentListView.as_view(), name="assignment-list"),
    path("assignments/upload/", AssignmentCreateView.as_view(), name="assignment-create"),
    path("assignments/submit/", AssignmentSubmissionCreateView.as_view(), name="assignment-submit"),
]
