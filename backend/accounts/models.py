"""
Accounts Models - User Profiles, Badges, Achievements
======================================================
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile with gamification data."""
    LEVEL_CHOICES = [(i, f'Level {i}') for i in range(1, 101)]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    xp_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    streak_days = models.IntegerField(default=0)
    total_badges = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.username} - Level {self.level} ({self.xp_points} XP)"

    def calculate_level(self):
        """Calculate level based on XP (every 500 XP = 1 level)."""
        self.level = max(1, self.xp_points // 500 + 1)
        self.save()

    def add_xp(self, amount, reason=''):
        """Add XP and recalculate level."""
        self.xp_points += amount
        self.calculate_level()
        # Log the XP transaction
        from gamebased.models import XPTransaction
        XPTransaction.objects.create(user=self.user, amount=amount, reason=reason)


class Badge(models.Model):
    """Achievement badges that users can earn."""
    BADGE_TYPES = [
        ('achievement', '🏆 Achievement'),
        ('course', '📚 Course'),
        ('streak', '🔥 Streak'),
        ('quiz', '🎯 Quiz'),
        ('special', '⭐ Special'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🏅')  # Emoji icon
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES, default='achievement')
    xp_reward = models.IntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'badges'

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserBadge(models.Model):
    """Junction table: which badges each user has earned."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_badges'
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} earned {self.badge.name}"


class Achievement(models.Model):
    """Achievements that unlock automatically based on conditions."""
    CONDITION_TYPES = [
        ('xp_milestone', 'XP Milestone'),
        ('quiz_count', 'Quiz Count'),
        ('streak_days', 'Streak Days'),
        ('course_complete', 'Course Completed'),
        ('badge_count', 'Badge Count'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    condition_type = models.CharField(max_length=30, choices=CONDITION_TYPES)
    condition_value = models.IntegerField()
    xp_reward = models.IntegerField(default=100)
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'achievements'

    def __str__(self):
        return f"{self.name} ({self.condition_type}: {self.condition_value})"
