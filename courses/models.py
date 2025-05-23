from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
import os

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses')
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class Page(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=120)
    content = models.TextField()
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - Page {self.order}: {self.title}"

class CourseQRCode(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='qr_code', primary_key=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"QR Code for {self.course.title}"

    def generate_qr_code(self):
        try:
            # Generate new UUID for the code
            self.code = uuid.uuid4()
            
            # Use course ID and UUID combination as QR code content to ensure uniqueness
            qr_content = f"course:{self.course.id}:{self.code}"
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # Use higher error correction level
                box_size=12,  # Increase QR code size
                border=4,
            )
            qr.add_data(qr_content)
            qr.make(fit=True)

            # Generate clearer image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Increase image size
            img = img.resize((400, 400), Image.Resampling.LANCZOS)
            
            # Delete old QR code image if exists
            if self.qr_image:
                try:
                    os.remove(self.qr_image.path)
                except:
                    pass
            
            buffer = BytesIO()
            img.save(buffer, format='PNG', quality=95)  # Use higher quality PNG
            filename = f'qr_code_{self.code}.png'
            self.qr_image.save(filename, File(buffer), save=False)
            
            return True
        except Exception as e:
            print(f"Error generating QR code: {str(e)}")
            return False

    def save(self, *args, **kwargs):
        if not self.qr_image or not self.code:
            if not self.generate_qr_code():
                raise Exception("Failed to generate QR code")
        super().save(*args, **kwargs)

class CourseEnrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
