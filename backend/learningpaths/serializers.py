from rest_framework import serializers
from .models import Subject, Course, CourseModule, Lesson, LearningPath, Enrollment, LessonProgress


class SubjectSerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'icon', 'color', 'course_count']

    def get_course_count(self, obj):
        return obj.courses.filter(is_published=True).count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'lesson_type', 'resource_url', 'order', 'xp_reward']


class CourseModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = CourseModule
        fields = ['id', 'title', 'description', 'order', 'duration_minutes', 'lessons']


class CourseListSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'subject', 'difficulty', 'duration_hours',
                  'thumbnail_url', 'instructor_name', 'xp_reward', 'enrollment_count', 'lesson_count', 'created_at']

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(module__course=obj).count()


class CourseDetailSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    modules = CourseModuleSerializer(many=True, read_only=True)
    enrollment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'subject', 'difficulty', 'duration_hours',
                  'thumbnail_url', 'instructor_name', 'xp_reward', 'modules', 'enrollment_count', 'created_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'enrolled_at', 'completed', 'completed_at', 'progress_percent']


class LearningPathSerializer(serializers.ModelSerializer):
    courses = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = LearningPath
        fields = ['id', 'name', 'description', 'courses', 'is_adaptive', 'recommended_for', 'created_at']
