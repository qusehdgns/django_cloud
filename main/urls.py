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
from main import views

urlpatterns = [
    # Login 페이지
    path('', views.login, name="login"),
    # 죄측 Index 바
    path('index', views.index, name="index"),
    # profile
    path('profile', views.profile, name="profile"),
    # sign in(회원가입)
    path('sign_in', views.sign_in, name="sign_in"),
    # id 중복 확인
    path('idcheck', views.idcheck, name='idcheck'),
    # id 찾기 및 pw 재설정
    path('find_id_reset_pw', views.find_id_reset_pw, name="find_id_reset_pw"),
    # logout
    path('logout', views.logout, name='logout'),
    # Team Storage 이동
    path('movetots', views.movetots, name='movetots'),
    # pw 재설정 url 이동
    path('movetoresetpw', views.movetoresetpw, name='movetoresetpw'),
    # master 페이지 이동
    path('movetotsmaster', views.movetotsmaster, name='movetotsmaster'),
    # 상위 폴더로 이동
    path('uptofolder', views.uptofolder, name='uptofolder'),
    # 프로필 수정
    path('changeprofile', views.changeprofile, name='changeprofile'),
    # 파일 다운로드
    path('download', views.download, name="download"),
    # Zipping
    path('zipping', views.zipping, name="zipping"),
    # zip down
    path('zipdownload', views.zipdownload, name="zipdownload"),
    # Folder list 함수
    path('folderlist', views.folderlist, name="folderlist"),
    # 회원 탈퇴 함수
    path('deleteuser', views.deleteuser, name="deleteuser"),
    # 아이디 찾기 함수
    path('findid', views.findid, name="findid"),
    # 사용자 검색 함수
    path('checkuser', views.checkuser, name="checkuser"),
    # 비밀번호 재설정 함수
    path('resetpw', views.resetpw, name="resetpw"),
    # 이모티콘 변경 함수
    path('changeemo', views.changeemo, name="changeemo"),
]

