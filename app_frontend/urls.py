# app_frontend/urls.py
from django.urls import path
from .views import (index, rock_sample, core_analysis)

app_name = 'frontend'

urlpatterns = [
    path('', index, name='index'),
    # path('tools/', tools, name="tools"),
    path('tools/rock_sample/', rock_sample, name="rock_sample"),
    path('tools/core_analysis/', core_analysis, name='core_analysis'),

]
