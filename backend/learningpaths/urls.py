from django.urls import path
from . import views

urlpatterns = [
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='course-enroll'),
    path('lessons/<int:lesson_id>/complete/', views.complete_lesson, name='lesson-complete'),
    path('my-enrollments/', views.MyEnrollmentsView.as_view(), name='my-enrollments'),
    path('paths/', views.LearningPathListView.as_view(), name='path-list'),
    path('recommendations/', views.adaptive_recommendations, name='recommendations'),
]
