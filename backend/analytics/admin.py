from django.contrib import admin
from .models import ActivityLog, DailyProgress, CourseAnalytics, UserAnalytics, WeeklyReport

admin.site.register(ActivityLog)
admin.site.register(DailyProgress)
admin.site.register(CourseAnalytics)
admin.site.register(UserAnalytics)
admin.site.register(WeeklyReport)
