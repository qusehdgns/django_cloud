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
from master import views

urlpatterns = [
    # Team Storage Master 관리 페이지
    path('', views.ts_master, name="ts_master"),
    # Team Storage 공지사항 페이지
    path('ts_notice_upload', views.ts_notice_upload, name="ts_notice_upload"),
    # Team Notice 공지사항 중복확인
    path('notice_check', views.notice_check, name="notice_check"),
    # Team Notice 수정 페이지
    path('ts_notice_update', views.ts_notice_update, name="ts_notice_update"),
    # Notice 삭제 함수
    path('noticedelete', views.noticedelete, name="noticedelete"),
    # Master invite User 탐색
    path('userlist', views.userlist, name="userlist"),
    # invite 함수
    path('invite', views.invite, name="invite"),
    # ban 함수
    path('ban', views.ban, name="ban"),
    # change authority 함수
    path('change_auth', views.change_auth, name="change_auth"),
    # 마스터 권한 이동
    path('givemaster', views.givemaster, name="givemaster"),
]
