from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Subject, Course, Lesson, LearningPath, Enrollment, LessonProgress
from .serializers import (SubjectSerializer, CourseListSerializer, CourseDetailSerializer,
                           EnrollmentSerializer, LearningPathSerializer)


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [AllowAny]


class CourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['subject', 'difficulty']
    search_fields = ['title', 'description', 'instructor_name']

    def get_queryset(self):
        return Course.objects.filter(is_published=True).select_related('subject')


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Course.objects.filter(is_published=True).prefetch_related('modules__lessons')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request, course_id):
    """POST /api/learningpaths/courses/<id>/enroll/ - Enroll in a course."""
    course = get_object_or_404(Course, id=course_id, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        return Response({'message': f'🎉 Enrolled in {course.title}!', 'enrolled': True}, status=status.HTTP_201_CREATED)
    return Response({'message': 'Already enrolled in this course.', 'enrolled': False})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_lesson(request, lesson_id):
    """POST /api/learningpaths/lessons/<id>/complete/ - Mark lesson as completed."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    time_spent = request.data.get('time_spent', 0)

    progress, created = LessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson,
        defaults={'completed': True, 'completed_at': timezone.now(), 'time_spent': time_spent}
    )

    xp_earned = 0
    if created:
        xp_earned = lesson.xp_reward
        profile = request.user.profile
        profile.xp_points += xp_earned
        profile.calculate_level()
        from gamebased.models import XPTransaction
        XPTransaction.objects.create(user=request.user, amount=xp_earned, reason=f'Completed lesson: {lesson.title}')

        # Update course enrollment progress
        course = lesson.module.course
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            total_lessons = Lesson.objects.filter(module__course=course).count()
            done_lessons = LessonProgress.objects.filter(user=request.user, lesson__module__course=course, completed=True).count()
            enrollment.progress_percent = (done_lessons / total_lessons * 100) if total_lessons else 0
            if enrollment.progress_percent >= 100:
                enrollment.completed = True
                enrollment.completed_at = timezone.now()
                profile.xp_points += course.xp_reward
                profile.calculate_level()
            enrollment.save()
        except Enrollment.DoesNotExist:
            pass

    return Response({'message': '✅ Lesson completed!', 'xp_earned': xp_earned, 'first_time': created})


class MyEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).select_related('course__subject')


class LearningPathListView(generics.ListAPIView):
    queryset = LearningPath.objects.prefetch_related('courses')
    serializer_class = LearningPathSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def adaptive_recommendations(request):
    """GET /api/learningpaths/recommendations/ - Recommend courses based on user activity."""
    enrolled_ids = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    recommended = Course.objects.filter(is_published=True).exclude(id__in=enrolled_ids).select_related('subject')[:6]
    serializer = CourseListSerializer(recommended, many=True)
    return Response({'recommendations': serializer.data})
