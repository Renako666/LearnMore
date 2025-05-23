from django.urls import path
from . import views

urlpatterns = [
    path('learner/', views.learner_dashboard, name='learner_dashboard'),
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
]
