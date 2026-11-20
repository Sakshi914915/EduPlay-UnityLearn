"""
Game-Based Learning Views - Quiz, Leaderboard, XP
"""
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Category, Quiz, Question, Option, QuizAttempt, QuizAttemptAnswer, XPTransaction, Leaderboard
from .serializers import (
    CategorySerializer, QuizListSerializer, QuizDetailSerializer,
    QuizAttemptSerializer, LeaderboardSerializer, XPTransactionSerializer
)


class CategoryListView(generics.ListAPIView):
    """GET /api/gamebased/categories/ - All quiz categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class QuizListView(generics.ListAPIView):
    """GET /api/gamebased/quizzes/ - List all published quizzes."""
    serializer_class = QuizListSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['category', 'difficulty']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Quiz.objects.filter(is_published=True).select_related('category', 'created_by')


class QuizDetailView(generics.RetrieveAPIView):
    """GET /api/gamebased/quizzes/<id>/ - Quiz with all questions."""
    serializer_class = QuizDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Quiz.objects.filter(is_published=True).prefetch_related('questions__options')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request, quiz_id):
    """
    POST /api/gamebased/quizzes/<id>/submit/
    Body: { "answers": [{"question_id": 1, "option_id": 3}, ...], "time_taken": 240 }
    Returns: score, XP earned, pass/fail status
    """
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    answers_data = request.data.get('answers', [])
    time_taken = request.data.get('time_taken', 0)

    # Calculate score
    score = 0
    max_score = 0
    attempt_answers = []

    for answer in answers_data:
        question_id = answer.get('question_id')
        option_id = answer.get('option_id')
        try:
            question = Question.objects.get(id=question_id, quiz=quiz)
            max_score += question.points
            option = Option.objects.get(id=option_id, question=question) if option_id else None
            is_correct = option.is_correct if option else False
            if is_correct:
                score += question.points
            attempt_answers.append({'question': question, 'option': option, 'is_correct': is_correct})
        except (Question.DoesNotExist, Option.DoesNotExist):
            continue

    # Determine pass/fail (60% to pass)
    passed = (score / max_score >= 0.6) if max_score > 0 else False

    # Calculate XP earned
    xp_earned = int(quiz.xp_reward * (score / max_score)) if max_score > 0 else 0

    # Create attempt record
    attempt = QuizAttempt.objects.create(
        user=request.user, quiz=quiz, score=score, max_score=max_score,
        time_taken=time_taken, passed=passed, xp_earned=xp_earned
    )

    # Save individual answers
    for a in attempt_answers:
        QuizAttemptAnswer.objects.create(
            attempt=attempt, question=a['question'],
            selected_option=a['option'], is_correct=a['is_correct']
        )

    # Award XP to user
    if xp_earned > 0:
        profile = request.user.profile
        profile.xp_points += xp_earned
        profile.calculate_level()
        XPTransaction.objects.create(user=request.user, amount=xp_earned, reason=f'Completed quiz: {quiz.title}')

        # Update leaderboard
        lb, _ = Leaderboard.objects.get_or_create(user=request.user)
        lb.total_xp += xp_earned
        lb.week_xp += xp_earned
        lb.month_xp += xp_earned
        lb.quizzes_completed += 1
        lb.save()

    return Response({
        'score': score,
        'max_score': max_score,
        'percentage': round((score / max_score * 100), 1) if max_score else 0,
        'passed': passed,
        'xp_earned': xp_earned,
        'time_taken': time_taken,
        'message': '🎉 Well done! Quiz completed!' if passed else '😔 Keep practicing! You can do it!',
    })


class MyAttemptsView(generics.ListAPIView):
    """GET /api/gamebased/my-attempts/ - User's quiz history."""
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).select_related('quiz')


class GameLeaderboardView(generics.ListAPIView):
    """GET /api/gamebased/leaderboard/ - Top 20 players."""
    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Leaderboard.objects.select_related('user').order_by('-total_xp')[:20]
