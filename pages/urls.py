from django.urls import path
from . import views

urlpatterns = [
    
    path('courses/<slug:course_slug>/', views.course_detail, name='page_detail'),
    path('', views.course_list, name='home'),   # 👈 ADD THIS
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:course_slug>/', views.chapter_list, name='chapter_list'),
    path('course/<int:course_id>/assignments/', views.assignment_list, name='assignment_list'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path(
        'courses/<slug:course_slug>/<slug:chapter_slug>/<slug:page_slug>/',
        views.page_detail,
        name='page_detail'
    ),
]
