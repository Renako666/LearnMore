from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<uuid:course_id>/', views.course_detail, name='course_detail'),
    path('<uuid:course_id>/join/', views.join_course, name='join_course'),
    path('<uuid:course_id>/edit/', views.course_edit, name='course_edit'),
    path('<uuid:course_id>/page/create/', views.page_create, name='page_create'),
    path('<uuid:course_id>/page/<int:page_id>/edit/', views.page_edit, name='page_edit'),
    path('<uuid:course_id>/page/<int:page_id>/delete/', views.page_delete, name='page_delete'),
    path('<uuid:course_id>/page/<int:page_id>/view/', views.page_view, name='page_view'),
    path('<uuid:course_id>/reorder/', views.reorder_pages, name='reorder_pages'),
    path('<uuid:course_id>/archive/', views.course_archive, name='course_archive'),
    path('<uuid:course_id>/qrcode/', views.generate_qr_code, name='generate_qr_code'),
    path('upload-qr-code/', views.upload_qr_code, name='upload_qr_code'),
]
