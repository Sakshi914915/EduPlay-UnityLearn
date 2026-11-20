from django.urls import path
from . import views

urlpatterns = [
    path('templates/', views.ContentTemplateListView.as_view(), name='template-list'),
    path('templates/<int:pk>/', views.ContentTemplateDetailView.as_view(), name='template-detail'),
    path('drafts/', views.ContentDraftListView.as_view(), name='draft-list'),
    path('drafts/<int:pk>/', views.ContentDraftDetailView.as_view(), name='draft-detail'),
    path('drafts/<int:draft_id>/publish/', views.publish_draft, name='draft-publish'),
    path('media/', views.MediaAssetListView.as_view(), name='media-list'),
    path('quiz-builder/', views.CustomQuizBuilderListView.as_view(), name='quiz-builder-list'),
    path('quiz-builder/<int:pk>/', views.CustomQuizBuilderDetailView.as_view(), name='quiz-builder-detail'),
    path('quiz-builder/<int:quiz_id>/publish/', views.publish_custom_quiz, name='quiz-builder-publish'),
]
