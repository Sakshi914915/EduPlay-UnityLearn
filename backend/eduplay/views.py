"""
EduPlay - Main API Root and System Info Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    🎮 EduPlay - UnityLearn: Central API Directory
    ==============================================
    All 6 modules of the Gamified Learning Platform are accessible below.
    Click any link to inspect live data from the Supabase PostgreSQL database.
    """
    return Response({
        'platform': 'EduPlay - UnityLearn (Gamified Learning Experience Platform)',
        'database': 'Supabase PostgreSQL (Live)',
        'status': 'Online ✅',
        'auth_endpoints': {
            'obtain_jwt_token': request.build_absolute_uri('/api/token/'),
            'refresh_jwt_token': request.build_absolute_uri('/api/token/refresh/'),
            'login': request.build_absolute_uri('/api/accounts/login/'),
            'register': request.build_absolute_uri('/api/accounts/register/'),
        },
        'module_0_accounts_and_gamification': {
            'user_profile': request.build_absolute_uri('/api/accounts/profile/'),
            'global_xp_leaderboard': request.build_absolute_uri('/api/accounts/leaderboard/'),
            'all_badges': request.build_absolute_uri('/api/accounts/badges/'),
        },
        'module_1_game_based_learning': {
            'quiz_categories': request.build_absolute_uri('/api/gamebased/categories/'),
            'quizzes_list': request.build_absolute_uri('/api/gamebased/quizzes/'),
            'game_leaderboard': request.build_absolute_uri('/api/gamebased/leaderboard/'),
            'user_quiz_attempts': request.build_absolute_uri('/api/gamebased/my-attempts/'),
        },
        'module_2_interactive_simulations': {
            'simulation_categories': request.build_absolute_uri('/api/simulations/categories/'),
            'all_simulations': request.build_absolute_uri('/api/simulations/'),
            'experiments': request.build_absolute_uri('/api/simulations/experiments/'),
        },
        'module_3_adaptive_learning_paths': {
            'subjects': request.build_absolute_uri('/api/learningpaths/subjects/'),
            'courses': request.build_absolute_uri('/api/learningpaths/courses/'),
            'my_enrollments': request.build_absolute_uri('/api/learningpaths/my-enrollments/'),
            'learning_paths': request.build_absolute_uri('/api/learningpaths/paths/'),
            'ai_recommendations': request.build_absolute_uri('/api/learningpaths/recommendations/'),
        },
        'module_4_collaborative_learning': {
            'study_groups': request.build_absolute_uri('/api/collaborative/groups/'),
            'forums': request.build_absolute_uri('/api/collaborative/forums/'),
            'forum_posts': request.build_absolute_uri('/api/collaborative/posts/'),
            'peer_reviews': request.build_absolute_uri('/api/collaborative/reviews/'),
            'announcements': request.build_absolute_uri('/api/collaborative/announcements/'),
        },
        'module_5_performance_analytics': {
            'dashboard_stats': request.build_absolute_uri('/api/analytics/dashboard/'),
            'activity_log': request.build_absolute_uri('/api/analytics/activity/'),
            'daily_progress': request.build_absolute_uri('/api/analytics/daily-progress/'),
            'weekly_reports': request.build_absolute_uri('/api/analytics/weekly-reports/'),
            'subject_performance': request.build_absolute_uri('/api/analytics/performance/'),
        },
        'module_6_content_authoring': {
            'content_templates': request.build_absolute_uri('/api/authoring/templates/'),
            'content_drafts': request.build_absolute_uri('/api/authoring/drafts/'),
            'custom_quiz_builder': request.build_absolute_uri('/api/authoring/quiz-builder/'),
            'media_assets': request.build_absolute_uri('/api/authoring/media/'),
        },
    })
