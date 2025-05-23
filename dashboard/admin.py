from django.contrib import admin
from .models import LearnerProgress, PageView

@admin.register(LearnerProgress)
class LearnerProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'completed', 'started_at', 'completed_at')
    list_filter = ('completed', 'started_at')
    search_fields = ('user__username', 'course__title')
    date_hierarchy = 'started_at'

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'page', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('user__username', 'page__title')
    date_hierarchy = 'viewed_at'
