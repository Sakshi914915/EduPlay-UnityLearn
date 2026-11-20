"""
Module 6: Content Authoring & Customization Tools
"""
from django.db import models
from django.contrib.auth.models import User


class ContentTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('quiz', '📝 Quiz Template'),
        ('lesson', '📖 Lesson Template'),
        ('simulation', '🔬 Simulation Template'),
        ('course', '📚 Course Template'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    template_type = models.CharField(max_length=15, choices=TEMPLATE_TYPES)
    template_data = models.JSONField(default=dict)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_templates')
    is_public = models.BooleanField(default=True)
    downloads_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content_templates'

    def __str__(self):
        return f"{self.name} [{self.template_type}]"


class ContentDraft(models.Model):
    STATUS_CHOICES = [('draft', '📝 Draft'), ('review', '👀 Under Review'), ('published', '✅ Published')]
    CONTENT_TYPES = [('quiz', 'Quiz'), ('lesson', 'Lesson'), ('article', 'Article')]

    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_drafts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    content_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content_drafts'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} [{self.status}]"


class MediaAsset(models.Model):
    ASSET_TYPES = [
        ('image', '🖼️ Image'),
        ('video', '🎥 Video'),
        ('audio', '🎵 Audio'),
        ('document', '📄 Document'),
    ]

    name = models.CharField(max_length=200)
    file_url = models.URLField()
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_assets')
    file_size = models.BigIntegerField(default=0, help_text='File size in bytes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'media_assets'

    def __str__(self):
        return f"{self.name} [{self.asset_type}]"


class CustomQuizBuilder(models.Model):
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    questions_data = models.JSONField(default=list)
    passing_score = models.IntegerField(default=60)
    time_limit = models.IntegerField(default=15, help_text='Minutes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_quizzes')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'custom_quiz_builder'

    def __str__(self):
        return f"{self.title} ({'Published' if self.is_published else 'Draft'})"
