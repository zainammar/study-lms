from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='home'),   # 👈 ADD THIS
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:course_slug>/', views.chapter_list, name='chapter_list'),
    path(
        'courses/<slug:course_slug>/<slug:chapter_slug>/<slug:page_slug>/',
        views.page_detail,
        name='page_detail'
    ),
]
