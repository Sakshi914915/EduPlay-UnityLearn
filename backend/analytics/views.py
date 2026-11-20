from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta, date

from .models import ActivityLog, DailyProgress, WeeklyReport
from .serializers import ActivityLogSerializer, DailyProgressSerializer, WeeklyReportSerializer
from accounts.models import UserProfile
from gamebased.models import QuizAttempt, XPTransaction
from learningpaths.models import Enrollment, LessonProgress


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """GET /api/analytics/dashboard/ - Comprehensive dashboard data."""
    user = request.user
    profile = user.profile

    # XP per day for last 7 days
    today = date.today()
    xp_chart = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        dp = DailyProgress.objects.filter(user=user, date=day).first()
        xp_chart.append({
            'date': day.strftime('%a'),
            'xp': dp.xp_earned if dp else 0
        })

    # Recent activity
    recent_activities = ActivityLog.objects.filter(user=user)[:5]
    activities_data = ActivityLogSerializer(recent_activities, many=True).data

    # Enrollment count
    enrollments = Enrollment.objects.filter(user=user)
    completed_courses = enrollments.filter(completed=True).count()

    # Quiz stats
    attempts = QuizAttempt.objects.filter(user=user)
    avg_score = 0
    if attempts.exists():
        total_pct = sum(a.percentage for a in attempts)
        avg_score = round(total_pct / attempts.count(), 1)

    return Response({
        'profile': {
            'xp_points': profile.xp_points,
            'level': profile.level,
            'streak_days': profile.streak_days,
            'total_badges': profile.total_badges,
        },
        'stats': {
            'courses_enrolled': enrollments.count(),
            'courses_completed': completed_courses,
            'quizzes_completed': attempts.count(),
            'avg_quiz_score': avg_score,
        },
        'xp_chart': xp_chart,
        'recent_activities': activities_data,
    })


class ActivityLogView(generics.ListAPIView):
    """GET /api/analytics/activity/ - Paginated activity log."""
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ActivityLog.objects.filter(user=self.request.user)


class DailyProgressView(generics.ListAPIView):
    """GET /api/analytics/daily-progress/ - Last 30 days progress."""
    serializer_class = DailyProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        since = date.today() - timedelta(days=30)
        return DailyProgress.objects.filter(user=self.request.user, date__gte=since)


class WeeklyReportView(generics.ListAPIView):
    """GET /api/analytics/weekly-reports/ - Weekly summary reports."""
    serializer_class = WeeklyReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WeeklyReport.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def performance_overview(request):
    """GET /api/analytics/performance/ - Quiz performance breakdown."""
    user = request.user
    attempts = QuizAttempt.objects.filter(user=user).select_related('quiz__category')

    subject_scores = {}
    for attempt in attempts:
        subject = attempt.quiz.category.name
        if subject not in subject_scores:
            subject_scores[subject] = {'total': 0, 'count': 0}
        subject_scores[subject]['total'] += attempt.percentage
        subject_scores[subject]['count'] += 1

    performance = [
        {'subject': k, 'avg_score': round(v['total'] / v['count'], 1)}
        for k, v in subject_scores.items()
    ]

    return Response({'subject_performance': performance})
