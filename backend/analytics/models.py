"""
Module 5: Performance Analytics & Progress Tracking
"""
from django.db import models
from django.contrib.auth.models import User


class ActivityLog(models.Model):
    ACTIVITY_TYPES = [
        ('quiz', '📝 Quiz'),
        ('lesson', '📖 Lesson'),
        ('simulation', '🔬 Simulation'),
        ('login', '🔐 Login'),
        ('badge_earned', '🏅 Badge Earned'),
        ('course_enrolled', '📚 Course Enrolled'),
        ('course_completed', '🎓 Course Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=25, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    xp_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activity_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}: {self.title}"


class DailyProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_progress')
    date = models.DateField()
    lessons_completed = models.IntegerField(default=0)
    quizzes_completed = models.IntegerField(default=0)
    simulations_completed = models.IntegerField(default=0)
    xp_earned = models.IntegerField(default=0)
    time_spent_minutes = models.IntegerField(default=0)

    class Meta:
        db_table = 'daily_progress'
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} on {self.date}: {self.xp_earned} XP"


class CourseAnalytics(models.Model):
    course = models.OneToOneField('learningpaths.Course', on_delete=models.CASCADE, related_name='analytics')
    total_enrollments = models.IntegerField(default=0)
    completion_rate = models.FloatField(default=0.0)
    avg_score = models.FloatField(default=0.0)
    avg_time_hours = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_analytics'
        verbose_name_plural = 'Course Analytics'


class UserAnalytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    total_time_spent_hours = models.FloatField(default=0.0)
    avg_quiz_score = models.FloatField(default=0.0)
    strongest_subject = models.CharField(max_length=100, blank=True)
    weakest_subject = models.CharField(max_length=100, blank=True)
    learning_streak = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_analytics'
        verbose_name_plural = 'User Analytics'

    def __str__(self):
        return f"Analytics for {self.user.username}"


class WeeklyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_reports')
    week_start = models.DateField()
    week_end = models.DateField()
    lessons_done = models.IntegerField(default=0)
    quizzes_done = models.IntegerField(default=0)
    xp_earned = models.IntegerField(default=0)
    time_spent_hours = models.FloatField(default=0.0)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'weekly_reports'
        ordering = ['-week_start']

    def __str__(self):
        return f"{self.user.username} week of {self.week_start}"
