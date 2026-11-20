from rest_framework import serializers
from .models import ActivityLog, DailyProgress, WeeklyReport, UserAnalytics


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id', 'activity_type', 'title', 'description', 'xp_earned', 'created_at']


class DailyProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyProgress
        fields = ['id', 'date', 'lessons_completed', 'quizzes_completed',
                  'simulations_completed', 'xp_earned', 'time_spent_minutes']


class WeeklyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyReport
        fields = ['id', 'week_start', 'week_end', 'lessons_done', 'quizzes_done',
                  'xp_earned', 'time_spent_hours', 'generated_at']


class UserAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnalytics
        fields = ['total_time_spent_hours', 'avg_quiz_score', 'strongest_subject',
                  'weakest_subject', 'learning_streak', 'last_updated']
