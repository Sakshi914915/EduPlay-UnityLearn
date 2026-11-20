from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import StudyGroup, Forum, ForumPost, PostComment, PostLike, PeerReview, Announcement
from .serializers import (StudyGroupSerializer, ForumSerializer, ForumPostSerializer,
                           PostCommentSerializer, PeerReviewSerializer, AnnouncementSerializer)


class StudyGroupListView(generics.ListCreateAPIView):
    serializer_class = StudyGroupSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'subject']

    def get_queryset(self):
        return StudyGroup.objects.filter(is_private=False)

    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)
        group.members.add(self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_group(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    if group.members.count() >= group.max_members:
        return Response({'error': 'Group is full.'}, status=status.HTTP_400_BAD_REQUEST)
    group.members.add(request.user)
    return Response({'message': f'Joined {group.name}!'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_group(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    group.members.remove(request.user)
    return Response({'message': f'Left {group.name}.'})


class ForumListView(generics.ListAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    permission_classes = [AllowAny]


class ForumPostListView(generics.ListCreateAPIView):
    serializer_class = ForumPostSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['title', 'content']

    def get_queryset(self):
        forum_id = self.kwargs.get('forum_id')
        if forum_id:
            return ForumPost.objects.filter(forum_id=forum_id)
        return ForumPost.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ForumPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.views += 1
        post.save()
        return super().retrieve(request, *args, **kwargs)


class CommentListView(generics.ListCreateAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PostComment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post = get_object_or_404(ForumPost, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        return Response({'liked': False, 'likes': post.like_count})
    return Response({'liked': True, 'likes': post.like_count})


class PeerReviewListView(generics.ListCreateAPIView):
    serializer_class = PeerReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PeerReview.objects.filter(reviewee=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class AnnouncementListView(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [AllowAny]
