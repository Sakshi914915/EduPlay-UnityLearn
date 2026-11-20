from rest_framework import serializers
from .models import ContentTemplate, ContentDraft, MediaAsset, CustomQuizBuilder


class ContentTemplateSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = ContentTemplate
        fields = ['id', 'name', 'description', 'template_type', 'template_data',
                  'created_by_username', 'is_public', 'downloads_count', 'created_at']


class ContentDraftSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = ContentDraft
        fields = ['id', 'title', 'content_type', 'author_username', 'status', 'content_data', 'created_at', 'updated_at']


class MediaAssetSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    file_size_kb = serializers.SerializerMethodField()

    class Meta:
        model = MediaAsset
        fields = ['id', 'name', 'file_url', 'asset_type', 'uploaded_by_username', 'file_size', 'file_size_kb', 'created_at']

    def get_file_size_kb(self, obj):
        return round(obj.file_size / 1024, 1)


class CustomQuizBuilderSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomQuizBuilder
        fields = ['id', 'title', 'instructions', 'questions_data', 'passing_score',
                  'time_limit', 'created_by_username', 'is_published', 'question_count', 'created_at', 'updated_at']

    def get_question_count(self, obj):
        return len(obj.questions_data) if isinstance(obj.questions_data, list) else 0
