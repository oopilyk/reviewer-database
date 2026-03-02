from django.contrib import admin
from .models import Reviewer, ReviewerSubjectAreas, ReviewerHistory


@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    list_display = ['id', 'fname', 'lname', 'email', 'status', 'panel_id', 'mission', 'cycle']
    list_filter = ['status', 'mission', 'cycle']
    search_fields = ['fname', 'lname', 'email']


@admin.register(ReviewerSubjectAreas)
class ReviewerSubjectAreasAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'area', 'priority']


@admin.register(ReviewerHistory)
class ReviewerHistoryAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'mission', 'cycle', 'htype']
