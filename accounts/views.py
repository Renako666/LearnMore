from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import UserRole
from .forms import UserRoleForm, UserProfileForm
from .decorators import admin_required

@login_required
def profile_view(request):
    """View for user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
@admin_required
def teacher_management(request):
    """Admin view for managing teachers"""
    # Get all teachers
    teachers = User.objects.filter(role__role=UserRole.TEACHER)
    
    # Get all students (can be promoted to teachers)
    students = User.objects.filter(role__role=UserRole.STUDENT)
    
    # Pagination
    paginator = Paginator(teachers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/teacher_management.html', {
        'page_obj': page_obj,
        'students': students,
    })

@login_required
@admin_required
def add_teacher(request):
    """View for adding a teacher"""
    if request.method == 'POST':
        form = UserRoleForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            user = get_object_or_404(User, id=user_id)
            
            # Update user role to teacher
            user_role = UserRole.objects.get(user=user)
            user_role.role = UserRole.TEACHER
            user_role.save()
            
            messages.success(request, f'User {user.username} has been successfully set as a teacher.')
            return redirect('teacher_management')
    else:
        form = UserRoleForm()
    
    return render(request, 'accounts/add_teacher.html', {'form': form})

@login_required
@admin_required
def remove_teacher(request, user_id):
    """View for removing a teacher role"""
    user = get_object_or_404(User, id=user_id)
    user_role = UserRole.objects.get(user=user)
    
    # Change teacher role to student
    user_role.role = UserRole.STUDENT
    user_role.save()
    
    messages.success(request, f'User {user.username} has been removed from the teacher role.')
    return redirect('teacher_management')
