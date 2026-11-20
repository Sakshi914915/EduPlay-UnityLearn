from django.contrib import admin
from .models import Category, Quiz, Question, Option, QuizAttempt, XPTransaction, Leaderboard


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'color']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'xp_reward', 'is_published', 'created_at']
    list_filter = ['difficulty', 'category', 'is_published']
    search_fields = ['title']


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'question_type', 'points']
    inlines = [OptionInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'max_score', 'passed', 'xp_earned', 'completed_at']
    list_filter = ['passed']


@admin.register(XPTransaction)
class XPTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'reason', 'created_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['rank', 'user', 'total_xp', 'week_xp', 'quizzes_completed']
    ordering = ['-total_xp']
