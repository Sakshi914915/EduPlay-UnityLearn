"""
Module 3: Adaptive Learning Paths - Course, Enrollment, Progress
"""
from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default='📚')
    color = models.CharField(max_length=7, default='#6C63FF')

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return f"{self.icon} {self.name}"


class Course(models.Model):
    DIFFICULTY = [('beginner', '🟢 Beginner'), ('intermediate', '🟡 Intermediate'), ('advanced', '🔴 Advanced')]

    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY, default='beginner')
    duration_hours = models.FloatField(default=5.0)
    thumbnail_url = models.URLField(blank=True)
    instructor_name = models.CharField(max_length=100, default='EduPlay Team')
    xp_reward = models.IntegerField(default=500)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return f"{self.title} [{self.difficulty}]"

    @property
    def enrollment_count(self):
        return self.enrollments.count()


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=30)

    class Meta:
        db_table = 'course_modules'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - Module {self.order}: {self.title}"


class Lesson(models.Model):
    LESSON_TYPES = [
        ('video', '🎥 Video'),
        ('reading', '📖 Reading'),
        ('quiz', '📝 Quiz'),
        ('simulation', '🔬 Simulation'),
    ]

    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    lesson_type = models.CharField(max_length=15, choices=LESSON_TYPES, default='reading')
    resource_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    xp_reward = models.IntegerField(default=25)

    class Meta:
        db_table = 'lessons'
        ordering = ['order']

    def __str__(self):
        return f"{self.title} [{self.lesson_type}]"


class LearningPath(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    courses = models.ManyToManyField(Course, related_name='paths')
    is_adaptive = models.BooleanField(default=False)
    recommended_for = models.TextField(blank=True, help_text='Who this path is recommended for')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'learning_paths'

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percent = models.FloatField(default=0.0)

    class Meta:
        db_table = 'enrollments'
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.IntegerField(default=0, help_text='Seconds spent on lesson')

    class Meta:
        db_table = 'lesson_progress'
        unique_together = ('user', 'lesson')


class SkillAssessment(models.Model):
    SKILL_LEVELS = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_assessments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    level = models.CharField(max_length=15, choices=SKILL_LEVELS, default='beginner')
    assessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skill_assessments'
