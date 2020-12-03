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
from api_gate import views

urlpatterns = [
    # 로그인
    path('api_login', views.api_login),
    # ID 확인
    path('api_idcheck', views.api_idcheck),
    # 회원가입
    path('api_signin', views.api_signin),
    # Storage 호출
    path('api_storage', views.api_storage),
    # 파일 다운로드
    path('api_download', views.api_download),
    # 파일 업로드
    path('api_upload', views.api_upload),
    # 파일 삭제
    path('api_delete', views.api_delete),
]

