from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from courses.models import Course, Page
from .models import LearnerProgress, PageView
from accounts.decorators import teacher_required, student_required

@login_required
@student_required
def learner_dashboard(request):
    # Get courses the user is learning
    in_progress = LearnerProgress.objects.filter(
        user=request.user,
        completed=False
    ).select_related('course', 'last_page')
    
    # Get courses the user has completed
    completed = LearnerProgress.objects.filter(
        user=request.user,
        completed=True
    ).select_related('course')
    
    # Calculate overall learning progress
    total_courses = in_progress.count() + completed.count()
    completion_rate = 0
    if total_courses > 0:
        completion_rate = (completed.count() / total_courses) * 100
    
    return render(request, 'dashboard/learner_dashboard.html', {
        'in_progress': in_progress,
        'completed': completed,
        'total_courses': total_courses,
        'completion_rate': completion_rate
    })

@login_required
@teacher_required
def instructor_dashboard(request):
    # Get courses created by the user
    courses = Course.objects.filter(creator=request.user)
    
    # Calculate stats for each course
    course_stats = []
    for course in courses:
        learners_count = LearnerProgress.objects.filter(course=course).count()
        completion_count = LearnerProgress.objects.filter(course=course, completed=True).count()
        completion_rate = 0
        if learners_count > 0:
            completion_rate = (completion_count / learners_count) * 100
        
        course_stats.append({
            'course': course,
            'learners_count': learners_count,
            'completion_count': completion_count,
            'completion_rate': completion_rate
        })
    
    # Calculate overall stats
    total_learners = LearnerProgress.objects.filter(course__in=courses).values('user').distinct().count()
    total_views = PageView.objects.filter(page__course__in=courses).count()
    
    # Prepare JSON data for the chart
    import json
    course_stats_json = json.dumps([{
        'course': {
            'title': stat['course'].title,
            'id': str(stat['course'].id)
        },
        'learners_count': stat['learners_count'],
        'completion_count': stat['completion_count'],
        'completion_rate': stat['completion_rate']
    } for stat in course_stats])
    
    return render(request, 'dashboard/instructor_dashboard.html', {
        'course_stats': course_stats,
        'course_stats_json': course_stats_json,
        'total_courses': courses.count(),
        'total_learners': total_learners,
        'total_views': total_views
    })
