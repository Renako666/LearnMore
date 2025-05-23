from django.contrib import admin
from .models import Course, Page

class PageInline(admin.TabularInline):
    model = Page
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at', 'archived')
    list_filter = ('archived', 'created_at')
    search_fields = ('title', 'creator__username')
    date_hierarchy = 'created_at'
    inlines = [PageInline]
