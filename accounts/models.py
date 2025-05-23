from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserRole(models.Model):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def is_admin(self):
        return self.role == self.ADMIN
    
    def is_teacher(self):
        return self.role == self.TEACHER
    
    def is_student(self):
        return self.role == self.STUDENT

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_courses = models.PositiveIntegerField(default=5)
    max_pages_per_course = models.PositiveIntegerField(default=20)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username

# Signal receivers: automatically create role and profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile_and_role(sender, instance, created, **kwargs):
    if created:
        # Create user role, default to student
        UserRole.objects.create(user=instance, role=UserRole.STUDENT)
        # Create user profile
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile_and_role(sender, instance, **kwargs):
    # Save user role and profile
    if not hasattr(instance, 'role'):
        UserRole.objects.create(user=instance, role=UserRole.STUDENT)
    else:
        instance.role.save()
    
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
