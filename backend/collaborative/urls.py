from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.StudyGroupListView.as_view(), name='group-list'),
    path('groups/<int:group_id>/join/', views.join_group, name='group-join'),
    path('groups/<int:group_id>/leave/', views.leave_group, name='group-leave'),
    path('forums/', views.ForumListView.as_view(), name='forum-list'),
    path('forums/<int:forum_id>/posts/', views.ForumPostListView.as_view(), name='forum-posts'),
    path('posts/', views.ForumPostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.ForumPostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', views.CommentListView.as_view(), name='comment-list'),
    path('posts/<int:post_id>/like/', views.toggle_like, name='post-like'),
    path('reviews/', views.PeerReviewListView.as_view(), name='review-list'),
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement-list'),
]
