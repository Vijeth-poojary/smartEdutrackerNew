from django.urls import path
from . import views

urlpatterns = [
    path('report-card/<int:student_id>/', views.ReportCardView.as_view(),name='report-card'),
    path('class-performance/', views.ClassPerformanceView.as_view(),name='class-performance'),
    path('top-performers/', views.TopPerformersView.as_view(),name='top-performers'),

]