from django.contrib import admin
from .models import UserProfile, Badge, UserBadge, Achievement


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'xp_points', 'level', 'streak_days', 'total_badges', 'created_at']
    list_filter = ['level']
    search_fields = ['user__username', 'user__email']
    ordering = ['-xp_points']


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'badge_type', 'xp_reward']
    list_filter = ['badge_type']
    search_fields = ['name']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge__badge_type']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'condition_type', 'condition_value', 'xp_reward']
