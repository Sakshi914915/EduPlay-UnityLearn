from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
    path('activity/', views.ActivityLogView.as_view(), name='activity-log'),
    path('daily-progress/', views.DailyProgressView.as_view(), name='daily-progress'),
    path('weekly-reports/', views.WeeklyReportView.as_view(), name='weekly-reports'),
    path('performance/', views.performance_overview, name='performance'),
]
