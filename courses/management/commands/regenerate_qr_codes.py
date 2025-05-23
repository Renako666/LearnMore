from django.core.management.base import BaseCommand
from courses.models import Course, CourseQRCode
from django.db import transaction

class Command(BaseCommand):
    help = 'Regenerate QR codes for all courses'

    def handle(self, *args, **options):
        self.stdout.write('Starting QR code regeneration...')
        
        with transaction.atomic():
            # Delete all existing QR codes
            CourseQRCode.objects.all().delete()
            self.stdout.write('Deleted all existing QR codes')
            
            # Get all active courses
            courses = Course.objects.filter(archived=False)
            count = 0
            
            for course in courses:
                try:
                    # Create new QR code
                    CourseQRCode.objects.create(course=course)
                    count += 1
                    self.stdout.write(f'Generated QR code for course: {course.title}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to generate QR code for course {course.title}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully regenerated {count} QR codes')) 