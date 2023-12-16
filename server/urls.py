# server/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app_db.urls')),
    path('', include('app_frontend.urls')),
]