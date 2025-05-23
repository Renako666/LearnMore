from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('teachers/', views.teacher_management, name='teacher_management'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/remove/<int:user_id>/', views.remove_teacher, name='remove_teacher'),
]
