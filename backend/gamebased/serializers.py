"""
Game-Based Learning Serializers
"""
from rest_framework import serializers
from .models import Category, Quiz, Question, Option, QuizAttempt, XPTransaction, Leaderboard


class CategorySerializer(serializers.ModelSerializer):
    quiz_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color', 'icon', 'quiz_count']

    def get_quiz_count(self, obj):
        return obj.quizzes.filter(is_published=True).count()


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_text', 'is_correct']


class OptionForStudentSerializer(serializers.ModelSerializer):
    """Options without revealing the correct answer."""
    class Meta:
        model = Option
        fields = ['id', 'option_text']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionForStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'points', 'order', 'options']


class QuizListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    question_count = serializers.IntegerField(read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'category', 'difficulty',
            'time_limit', 'xp_reward', 'question_count', 'created_by_username', 'created_at'
        ]


class QuizDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'category', 'difficulty',
            'time_limit', 'xp_reward', 'questions', 'question_count', 'created_at'
        ]


class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = QuizAttempt
        fields = [
            'id', 'quiz_title', 'score', 'max_score', 'percentage',
            'time_taken', 'passed', 'xp_earned', 'completed_at'
        ]


class XPTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = XPTransaction
        fields = ['id', 'amount', 'reason', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    full_name = serializers.SerializerMethodField()
    level = serializers.IntegerField(source='user.profile.level', default=1)

    class Meta:
        model = Leaderboard
        fields = ['rank', 'username', 'full_name', 'level', 'total_xp', 'week_xp', 'quizzes_completed']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
