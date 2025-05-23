from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LearnerProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='learner_progress')
    last_page = models.ForeignKey('courses.Page', on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'course']
    
    def __str__(self):
        status = "Completed" if self.completed else "In Progress"
        return f"{self.user.username} - {self.course.title}: {status}"
    
    def mark_as_completed(self):
        """Mark the course as completed and set completion timestamp"""
        self.completed = True
        self.completed_at = timezone.now()
        self.save()

class PageView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey('courses.Page', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
