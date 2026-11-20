from django.contrib import admin
from .models import StudyGroup, Forum, ForumPost, PostComment, PeerReview, Announcement

admin.site.register(StudyGroup)
admin.site.register(Forum)
admin.site.register(ForumPost)
admin.site.register(PostComment)
admin.site.register(PeerReview)
admin.site.register(Announcement)
