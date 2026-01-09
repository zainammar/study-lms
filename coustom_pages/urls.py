from django.urls import path
from .views import page_link

urlpatterns = [
    path('<slug:slug>/', page_link, name='page_link'),
]
