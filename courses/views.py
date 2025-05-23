from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q, Max
from django.core.paginator import Paginator
import qrcode
import io
from .models import Course, Page, CourseQRCode, CourseEnrollment
from .forms import CourseForm, PageForm, QRCodeUploadForm
from dashboard.models import LearnerProgress, PageView
from accounts.decorators import teacher_required, student_required
from django.db import IntegrityError
from PIL import Image

@login_required
def course_list(request):
    query = request.GET.get('q', '').strip()
    if hasattr(request.user, 'role') and request.user.role.is_teacher:
        courses = Course.objects.filter(creator=request.user)
    elif hasattr(request.user, 'role') and request.user.role.is_admin:
        courses = Course.objects.all()
    elif hasattr(request.user, 'role') and request.user.role.is_student:
        courses = Course.objects.filter(enrollments__student=request.user, enrollments__is_active=True)
    else:
        courses = Course.objects.none()
    if query:
        courses = courses.filter(Q(title__icontains=query) | Q(description__icontains=query))
    courses = courses.order_by('-created_at')
    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'courses/course_list.html', {
        'page_obj': page_obj,
        'query': query,
    })

@login_required
def upload_qr_code(request):
    if not request.user.role.is_student:
        return HttpResponseForbidden("Only students can join courses using QR codes.")
    
    if request.method == 'POST':
        form = QRCodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Get course object
                course = form.cleaned_data.get('qr_code_image')
                if course:
                    # Check if course is archived
                    if course.archived:
                        messages.error(request, 'This course has been archived and cannot be joined.')
                        return redirect('course_list')
                    
                    # Check if already enrolled
                    enrollment = CourseEnrollment.objects.filter(
                        student=request.user,
                        course=course
                    ).first()
                    
                    if enrollment:
                        if enrollment.is_active:
                            messages.info(request, f'You have already joined the course: {course.title}')
                        else:
                            # Reactivate existing enrollment
                            enrollment.is_active = True
                            enrollment.save()
                            messages.success(request, f'Successfully rejoined the course: {course.title}')
                    else:
                        # Create new enrollment
                        CourseEnrollment.objects.create(
                            student=request.user,
                            course=course
                        )
                        messages.success(request, f'Successfully joined the course: {course.title}')
                    
                    # Create or update learning progress
                    progress, created = LearnerProgress.objects.get_or_create(
                        user=request.user,
                        course=course
                    )
                    
                    # If newly joined course, set first page as current page
                    if created:
                        first_page = course.pages.order_by('order').first()
                        if first_page:
                            progress.last_page = first_page
                            progress.save()
                    
                    return redirect('course_detail', course_id=course.id)
                else:
                    messages.error(request, 'Failed to process QR code. Please try again.')
            except Exception as e:
                print(f"Error in upload_qr_code: {str(e)}")
                messages.error(request, 'An error occurred while processing the QR code. Please try again later.')
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = QRCodeUploadForm()
    
    return render(request, 'courses/upload_qr_code.html', {
        'form': form,
        'title': 'Scan to Join Course'
    })

@login_required
def course_create(request):
    if not request.user.role.is_teacher and not request.user.role.is_admin:
        return HttpResponseForbidden("Only teachers can create courses.")

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.creator = request.user
            course.save()  # Ensure a new UUID is generated
            try:
                # Try to create a QR code for this course
                CourseQRCode.objects.create(course=course)
            except IntegrityError:
                # If a QR code already exists for this course, ignore (should not happen)
                pass
            except Exception as e:
                messages.error(request, f"Failed to create QR code: {str(e)}")
                return render(request, 'courses/course_form.html', {'form': form})
            messages.success(request, 'Course created successfully!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()

    return render(request, 'courses/course_form.html', {'form': form})

@login_required
@teacher_required
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id, creator=request.user)
    pages = course.pages.all().order_by('order')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_edit', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/course_edit.html', {
        'course': course,
        'pages': pages,
        'form': form
    })

@login_required
@teacher_required
def page_create(request, course_id):
    course = get_object_or_404(Course, id=course_id, creator=request.user)
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.course = course
            # Set the order of the new page to max order + 1
            max_order = course.pages.aggregate(Max('order'))['order__max'] or 0
            page.order = max_order + 1
            page.save()
            messages.success(request, 'Page created successfully!')
            return redirect('course_edit', course_id=course.id)
    else:
        form = PageForm()
    
    return render(request, 'courses/page_editor.html', {
        'course': course,
        'form': form,
        'page': None,
        'is_new': True
    })

@login_required
@teacher_required
def page_edit(request, course_id, page_id):
    course = get_object_or_404(Course, id=course_id, creator=request.user)
    page = get_object_or_404(Page, id=page_id, course=course)
    
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            messages.success(request, 'Page updated successfully!')
            return redirect('course_edit', course_id=course.id)
    else:
        form = PageForm(instance=page)
    
    return render(request, 'courses/page_editor.html', {
        'course': course,
        'page': page,
        'form': form,
        'is_new': False
    })

@login_required
@teacher_required
def reorder_pages(request, course_id):
    if request.method == 'POST' and request.is_ajax():
        course = get_object_or_404(Course, id=course_id, creator=request.user)
        page_ids = request.POST.getlist('page_ids[]')
        
        for i, page_id in enumerate(page_ids, 1):
            Page.objects.filter(id=page_id, course=course).update(order=i)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@teacher_required
def page_delete(request, course_id, page_id):
    course = get_object_or_404(Course, id=course_id, creator=request.user)
    page = get_object_or_404(Page, id=page_id, course=course)
    
    if request.method == 'POST':
        # Delete the page
        page.delete()
        
        # Reorder remaining pages
        pages = course.pages.all().order_by('order')
        for i, p in enumerate(pages, 1):
            p.order = i
            p.save()
        
        messages.success(request, 'Page deleted successfully!')
        return redirect('course_edit', course_id=course.id)
    
    return redirect('course_edit', course_id=course.id)

@login_required
@teacher_required
def course_archive(request, course_id):
    course = get_object_or_404(Course, id=course_id, creator=request.user)
    
    if request.method == 'POST':
        course.archived = True
        course.save()
        messages.success(request, 'Course archived successfully!')
        return redirect('course_list')
    
    return redirect('course_edit', course_id=course.id)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, archived=False)
    pages = course.pages.all().order_by('order')
    
    # If user is logged in, check for learning progress
    progress = None
    if request.user.is_authenticated:
        progress = LearnerProgress.objects.filter(
            user=request.user,
            course=course
        ).first()
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'pages': pages,
        'progress': progress
    })

@login_required
def join_course(request, course_id):
    """Allow students to join a course"""
    course = get_object_or_404(Course, id=course_id, archived=False)
    
    # Check if user is already enrolled
    existing_progress = LearnerProgress.objects.filter(
        user=request.user,
        course=course
    ).exists()
    
    if existing_progress:
        messages.info(request, 'You are already enrolled in this course.')
    else:
        # Create new progress record
        progress = LearnerProgress(user=request.user, course=course)
        
        # Set first page as current page if available
        first_page = course.pages.order_by('order').first()
        if first_page:
            progress.last_page = first_page
        
        progress.save()
        messages.success(request, f'You have successfully joined the course "{course.title}"!')
    
    return redirect('course_detail', course_id=course.id)

@login_required
def page_view(request, course_id, page_id):
    course = get_object_or_404(Course, id=course_id, archived=False)
    page = get_object_or_404(Page, id=page_id, course=course)
    
    # Record page view
    PageView.objects.create(user=request.user, page=page)
    
    # Update learning progress
    progress, _ = LearnerProgress.objects.get_or_create(
        user=request.user,
        course=course
    )
    progress.last_page = page
    progress.save()
    
    # Check if this is the last page and all pages have been viewed
    if page.order == course.pages.count():
        # Get all pages for this course
        all_pages = course.pages.all()
        # Check if user has viewed all pages
        viewed_pages = PageView.objects.filter(
            user=request.user,
            page__in=all_pages
        ).values_list('page_id', flat=True).distinct()
        
        # If all pages have been viewed, mark course as completed
        if len(viewed_pages) == all_pages.count():
            progress.mark_as_completed()
            messages.success(request, f'Congratulations! You have completed the course "{course.title}"!')
    
    # Get all pages for navigation
    pages = course.pages.all().order_by('order')
    
    return render(request, 'courses/page_view.html', {
        'course': course,
        'current_page': page,
        'pages': pages,
        'progress': progress
    })

@login_required
def generate_qr_code(request, course_id):
    """
    Generate QR code for a course.
    This view should only be used for displaying QR codes, not for creating them.
    QR codes are created automatically when a CourseQRCode object is created.
    """
    course = get_object_or_404(Course, id=course_id)
    
    try:
        # Get the QR code object for this course
        course_qr = CourseQRCode.objects.get(course=course)
        
        # If QR code image doesn't exist, generate it
        if not course_qr.qr_image:
            course_qr.generate_qr_code()
            course_qr.refresh_from_db()
        
        # Return the stored QR code image
        if course_qr.qr_image:
            with open(course_qr.qr_image.path, 'rb') as f:
                return HttpResponse(f.read(), content_type='image/png')
        else:
            raise Exception("QR code image not found")
            
    except CourseQRCode.DoesNotExist:
        # If QR code doesn't exist, create it
        try:
            course_qr = CourseQRCode.objects.create(course=course)
            with open(course_qr.qr_image.path, 'rb') as f:
                return HttpResponse(f.read(), content_type='image/png')
        except Exception as e:
            print(f"Error creating QR code: {str(e)}")
            return HttpResponse("Failed to generate QR code", status=500)
    except Exception as e:
        print(f"Error retrieving QR code: {str(e)}")
        return HttpResponse("Failed to retrieve QR code", status=500)
