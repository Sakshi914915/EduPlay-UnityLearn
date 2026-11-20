from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudyGroup, Forum, ForumPost, PostComment, PeerReview, Announcement


class StudyGroupSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'description', 'subject', 'created_by_username',
                  'member_count', 'max_members', 'is_private', 'created_at']

    def get_member_count(self, obj):
        return obj.members.count()


class PostCommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'author_username', 'content', 'parent_comment', 'created_at']


class ForumPostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ForumPost
        fields = ['id', 'forum', 'title', 'content', 'author_username',
                  'pinned', 'views', 'like_count', 'comment_count', 'created_at']


class ForumSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Forum
        fields = ['id', 'title', 'description', 'subject', 'post_count', 'created_at']

    def get_post_count(self, obj):
        return obj.posts.count()


class PeerReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    reviewee_username = serializers.CharField(source='reviewee.username', read_only=True)

    class Meta:
        model = PeerReview
        fields = ['id', 'reviewer_username', 'reviewee_username', 'content_title', 'rating', 'feedback', 'created_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_by_username', 'target_audience', 'created_at']
