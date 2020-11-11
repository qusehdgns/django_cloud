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
    # Team Storage
    path('', views.team_storage, name="team_storage"),
    # Team Storage 폴더 추가
    path('tsaddfolder', views.tsaddfolder, name='tsaddfolder'),
    # Team Storage 하위 폴더로 이동
    path('tsmovefolder', views.tsmovefolder, name='tsmovefolder'),
    # Team Storage list 페이지
    path('team_storage_list', views.team_storage_list, name="team_storage_list"),
    # Team Storage 생성 페이지
    path('team_storage_create', views.team_storage_create, name="team_storage_create"),
    # Team Storage 파일 업로드 페이지
    path('ts_file_upload', views.ts_file_upload, name="ts_file_upload"),
    # personal storage 파일 업로드
    path('team_file_upload', views.team_file_upload, name='team_file_upload'),
    # Pesonal Storage 파일 삭제
    path('tsdeletefile', views.tsdeletefile, name="tsdeletefile"),
    # Team Storage 생성 시 Team Storage 이름 확인
    path('tsnamecheck', views.tsnamecheck, name="tsnamecheck"),
    # Team Storage 생성
    path('createteamstorage', views.createteamstorage, name="createteamstorage"),
    # Team Notice 페이지
    path('team_notice', views.team_notice, name="team_notice"),
    # Team Storage 탈퇴 함수
    path('tsexit', views.tsexit, name="tsexit"),
    # Team Storage 파일 중복 함수
    path('tsfilecheck', views.tsfilecheck, name="tsfilecheck"),
]
