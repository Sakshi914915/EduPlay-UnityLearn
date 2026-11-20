from django.contrib import admin
from .models import Subject, Course, CourseModule, Lesson, LearningPath, Enrollment, LessonProgress, SkillAssessment

admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(CourseModule)
admin.site.register(Lesson)
admin.site.register(LearningPath)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(SkillAssessment)
