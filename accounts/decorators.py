from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps

def admin_required(function):
    """Decorator to check if user is an admin"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role.is_admin():
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap

def teacher_required(function):
    """Decorator to check if user is a teacher"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'role') and (request.user.role.is_teacher() or request.user.role.is_admin()):
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap

def student_required(function):
    """Decorator to check if user is a student"""
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role.is_student():
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap
