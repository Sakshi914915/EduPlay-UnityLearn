"""
Module 1: Game-Based Learning Models
=====================================
Quiz, Question, Option, Attempt, XP, Leaderboard
"""
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Quiz categories (Math, Science, etc.)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6C63FF')  # Hex color
    icon = models.CharField(max_length=10, default='📚')

    class Meta:
        db_table = 'quiz_categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.icon} {self.name}"


class Quiz(models.Model):
    """A quiz with questions."""
    DIFFICULTY_CHOICES = [('easy', '🟢 Easy'), ('medium', '🟡 Medium'), ('hard', '🔴 Hard')]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    time_limit = models.IntegerField(default=15, help_text='Time limit in minutes')
    xp_reward = models.IntegerField(default=100)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quizzes'
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return f"{self.title} [{self.difficulty}]"

    @property
    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    """A question belonging to a quiz."""
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True / False'),
        ('fill_blank', 'Fill in the Blank'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPES, default='mcq')
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)
    explanation = models.TextField(blank=True, help_text='Explanation shown after answering')

    class Meta:
        db_table = 'quiz_questions'
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:60]}..."


class Option(models.Model):
    """Answer options for a question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz_options'

    def __str__(self):
        return f"{'✅' if self.is_correct else '❌'} {self.option_text}"


class QuizAttempt(models.Model):
    """Record of a user's quiz attempt."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)
    time_taken = models.IntegerField(default=0, help_text='Seconds taken')
    completed_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField(default=False)
    xp_earned = models.IntegerField(default=0)

    class Meta:
        db_table = 'quiz_attempts'
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}/{self.max_score})"

    @property
    def percentage(self):
        if self.max_score == 0:
            return 0
        return round((self.score / self.max_score) * 100, 1)


class QuizAttemptAnswer(models.Model):
    """Individual answer for each question in an attempt."""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz_attempt_answers'


class XPTransaction(models.Model):
    """Log of all XP earned by users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xp_transactions')
    amount = models.IntegerField()
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'xp_transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} +{self.amount} XP ({self.reason})"


class Leaderboard(models.Model):
    """Cached leaderboard data for performance."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard')
    total_xp = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    week_xp = models.IntegerField(default=0)
    month_xp = models.IntegerField(default=0)
    quizzes_completed = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['-total_xp']

    def __str__(self):
        return f"#{self.rank} {self.user.username} - {self.total_xp} XP"
