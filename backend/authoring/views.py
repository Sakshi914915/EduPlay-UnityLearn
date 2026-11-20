from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import ContentTemplate, ContentDraft, MediaAsset, CustomQuizBuilder
from .serializers import (ContentTemplateSerializer, ContentDraftSerializer,
                           MediaAssetSerializer, CustomQuizBuilderSerializer)


class ContentTemplateListView(generics.ListCreateAPIView):
    serializer_class = ContentTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContentTemplate.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ContentTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContentTemplate.objects.all()
    serializer_class = ContentTemplateSerializer
    permission_classes = [IsAuthenticated]


class ContentDraftListView(generics.ListCreateAPIView):
    serializer_class = ContentDraftSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContentDraft.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContentDraftDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContentDraftSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContentDraft.objects.filter(author=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def publish_draft(request, draft_id):
    draft = get_object_or_404(ContentDraft, id=draft_id, author=request.user)
    draft.status = 'published'
    draft.save()
    return Response({'message': f'✅ "{draft.title}" published successfully!'})


class MediaAssetListView(generics.ListCreateAPIView):
    serializer_class = MediaAssetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MediaAsset.objects.filter(uploaded_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class CustomQuizBuilderListView(generics.ListCreateAPIView):
    serializer_class = CustomQuizBuilderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomQuizBuilder.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CustomQuizBuilderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomQuizBuilderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomQuizBuilder.objects.filter(created_by=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def publish_custom_quiz(request, quiz_id):
    quiz = get_object_or_404(CustomQuizBuilder, id=quiz_id, created_by=request.user)
    quiz.is_published = True
    quiz.save()
    return Response({'message': f'🎉 Quiz "{quiz.title}" published!'})
