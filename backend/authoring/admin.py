from django.contrib import admin
from .models import ContentTemplate, ContentDraft, MediaAsset, CustomQuizBuilder

@admin.register(ContentTemplate)
class ContentTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'created_by', 'is_public', 'downloads_count', 'created_at']
    list_filter = ['template_type', 'is_public']
    search_fields = ['name', 'description']

@admin.register(ContentDraft)
class ContentDraftAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'author', 'status', 'updated_at']
    list_filter = ['status', 'content_type']
    search_fields = ['title']

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'asset_type', 'uploaded_by', 'created_at']
    list_filter = ['asset_type']

@admin.register(CustomQuizBuilder)
class CustomQuizBuilderAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_published', 'passing_score', 'time_limit', 'created_at']
    list_filter = ['is_published']
    search_fields = ['title']
