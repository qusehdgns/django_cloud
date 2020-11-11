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
from personal import views

urlpatterns = [
    # Personal Storage 페이지
    path('', views.personal_storage, name="personal_storage"),
    # Personal Storage 폴더 추가
    path('psaddfolder', views.psaddfolder, name='psaddfolder'),
    # Personal Storage 하위 폴더로 이동
    path('psmovefolder', views.psmovefolder, name='psmovefolder'),
    # Personal Storage 파일 업로드 페이지
    path('ps_file_upload', views.ps_file_upload, name="ps_file_upload"),
    # personal storage 파일 업로드
    path('personal_file_upload', views.personal_file_upload, name='personal_file_upload'),
    # Pesonal Storage 파일 삭제
    path('psdeletefile', views.psdeletefile, name="psdeletefile"),
    # 파일 중복 확인 함수
    path('psfilecheck', views.psfilecheck, name="psfilecheck"),
]
