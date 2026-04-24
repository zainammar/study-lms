from django.contrib import admin
from django.urls import path, include
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('fees/', include('students.urls')),
       path('', include('pages.urls')),
       path('', include('pages.urls')),
]



# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
