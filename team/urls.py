"""cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from team import views

urlpatterns = [
    path('', views.team_storage, name="team_storage"),
    path('team_storage_list', views.team_storage_list, name="team_storage_list"),
    path('team_storage_create', views.team_storage_create, name="team_storage_create"),
    path('ts_file_upload', views.ts_file_upload, name="ts_file_upload"),
    path('tsnamecheck', views.tsnamecheck, name="tsnamecheck"),
    path('createteamstorage', views.createteamstorage, name="createteamstorage"),
]
