from django.contrib import admin
from .models import Subscription, UserProfile, UserRole

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'max_courses', 'max_pages_per_course')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription')
    list_filter = ('subscription',)
    search_fields = ('user__username', 'user__email')

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    actions = ['make_teacher', 'make_student', 'make_admin']
    
    def make_teacher(self, request, queryset):
        queryset.update(role=UserRole.TEACHER)
    make_teacher.short_description = "Set selected users as teachers"
    
    def make_student(self, request, queryset):
        queryset.update(role=UserRole.STUDENT)
    make_student.short_description = "Set selected users as students"
    
    def make_admin(self, request, queryset):
        queryset.update(role=UserRole.ADMIN)
    make_admin.short_description = "Set selected users as administrators"
