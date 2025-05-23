from django import forms
from .models import Course, Page, CourseQRCode, CourseEnrollment
import cv2
import numpy as np
from django.core.exceptions import ValidationError

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

class QRCodeUploadForm(forms.Form):
    qr_code_image = forms.ImageField(
        label='Upload QR Code',
        help_text='Upload a QR code image to join a course',
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'lang': 'en',
            'data-browse': 'Choose File'
        })
    )

    def clean_qr_code_image(self):
        image = self.cleaned_data.get('qr_code_image')
        if not image:
            raise ValidationError('Please select a QR code image to upload.')
            
        try:
            # Check file size (limit to 5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Image size cannot exceed 5MB.')
            
            # Check file type
            if not image.content_type.startswith('image/'):
                raise ValidationError('Please upload a valid image file.')
            
            # Read image
            img_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValidationError('Unable to read image file. Please ensure the file format is correct.')
            
            # Image preprocessing
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Adaptive thresholding
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            
            # Create QR code detector
            qr_detector = cv2.QRCodeDetector()
            
            # Try to detect QR code in both original and preprocessed images
            retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(img)
            if not retval:
                print("DEBUG: QR code not detected in original image, trying preprocessed image")
                retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(thresh)
            
            if not retval:
                raise ValidationError('No QR code detected in the image. Please ensure:\n'
                                    '1. The image is clear and the QR code is complete\n'
                                    '2. The QR code is not obscured or damaged\n'
                                    '3. The image has adequate lighting')
            
            # Get the first detected QR code content
            qr_code = decoded_info[0]
            print(f"DEBUG: Detected QR code content: {qr_code}")
            
            # Validate QR code format
            if not qr_code.startswith('course:'):
                print(f"DEBUG: Invalid QR code format. Expected 'course:' prefix, got: {qr_code[:10]}...")
                raise ValidationError('Invalid course QR code. Please ensure you are using the correct course QR code.')
            
            try:
                # Parse QR code content
                parts = qr_code.split(':')
                if len(parts) != 3:
                    print(f"DEBUG: Invalid QR code format. Expected 3 parts, got {len(parts)}")
                    raise ValueError("Invalid QR code format")
                    
                _, course_id, code = parts
                print(f"DEBUG: Parsed QR code - Course ID: {course_id}, Code: {code}")
                
                # Find corresponding course
                course_qr = CourseQRCode.objects.get(
                    course_id=course_id,
                    code=code,
                    is_active=True
                )
                print(f"DEBUG: Found matching course: {course_qr.course.title}")
                return course_qr.course
            except ValueError as e:
                print(f"DEBUG: Error parsing QR code: {str(e)}")
                raise ValidationError('Invalid QR code format. Please ensure you are using the correct course QR code.')
            except CourseQRCode.DoesNotExist:
                print(f"DEBUG: No matching course found for ID: {course_id}, Code: {code}")
                raise ValidationError('QR code is invalid or expired. Please ensure you are using the latest course QR code.')
            
        except ValidationError:
            raise
        except Exception as e:
            print(f"QR code processing error: {str(e)}")
            raise ValidationError('Error processing QR code. Please try:\n'
                                '1. Using a clearer image\n'
                                '2. Ensuring the QR code is complete and unobstructed\n'
                                '3. Adjusting the image angle and lighting')
