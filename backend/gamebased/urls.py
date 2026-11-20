from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='quiz-categories'),
    path('quizzes/', views.QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/<int:quiz_id>/submit/', views.submit_quiz, name='quiz-submit'),
    path('my-attempts/', views.MyAttemptsView.as_view(), name='my-attempts'),
    path('leaderboard/', views.GameLeaderboardView.as_view(), name='game-leaderboard'),
]
