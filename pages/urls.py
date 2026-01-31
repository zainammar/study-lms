from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:course_slug>/detail/', views.course_detail, name='course_detail'),
    path('courses/<slug:course_slug>/chapters/', views.chapter_list, name='chapter_list'),
    path('course/<int:course_id>/assignments/', views.assignment_list, name='assignment_list'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path(
        'courses/<slug:course_slug>/<slug:chapter_slug>/<slug:page_slug>/',
        views.page_detail,
        name='page_detail'
    ),
    path('results/', views.results, name='results'),
     path(
        'course/<slug:course_slug>/live/',
        views.live_classes,
        name='live_classes'
    ),
]