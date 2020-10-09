from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse

import json

import os

# 데이터 베이스 연동 기능
# main App의 models.py 내부 class 선언
from main.models import User, StorageList
# master App의 models.py 내부 class 선언
from master.models import TeamStorage

# data 디렉토리 경로
data_location = "C:/Users/quseh/Desktop/workspace/django/Capstone/data"

# 웹 서버 경로
web_location = "C:/Users/quseh/Desktop/workspace/django/Capstone/cloud"

# 초기 디렉터리 저장
position = os.getcwd()

# http://localhost:8000/
# 초반 메인 Login 페이지 호출 및 로그인 수행 함수
def login(request):

    # 상위 폴더 이동
    os.chdir("..")

    # data 디렉토리 없을 시 실행
    if not os.path.exists("data"):
        # data 디렉토리 생성
        os.makedirs("data")
    
    # data 디렉토리로 이동
    os.chdir("./data")

    # personal 디렉토리 없을 시 실행
    if not os.path.exists("personal"):
        # personal 디렉토리 생성
        os.makedirs("personal")

    # team 디렉토리 없을 시 실행
    if not os.path.exists("team"):
        # team 디렉토리 생성
        os.makedirs("team")
    
    # 웹 서버 디렉토리로 이동
    os.chdir(position)

    # Post 형식 데이터가 들어오는지 확인
    if request.method == "POST":
        # Post 형식 데이터를 data 변수에 저장
        data = request.POST;

        # User 테이블에 사용자 id, pw 탐색
        if User.objects.filter(user_id = data['userid'], user_pw = data['userpw']).exists() == True :
            # 세션에 userid 담기
            request.session['userid'] = data['userid']

            # urls.py에 path 중 이름 personal_storage 호출
            return redirect('personal_storage')
        else:
            # 반환 html 문자열
            html = "<h1>로그인 실패</h1><input type='button' value='로그인 화면으로 이동' onclick='move();'></input>"
            html += "<script>function move(){location.href='/';}</script>"
            
            # 문자열 자체를 반환
            return HttpResponse(html)

    # Post 형식 데이터가 없을 시 Login.html 반환
    return render(request, 'Login.html')

# 사용자 정보를 표시하는 container html 함수 좌측 바를 담당
def index(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # User 테이블에서 Primary key가 userid인 레코드 호출
    # sql : select * from user where primary key = 변수userid;
    user_result = User.objects.get(pk = userid)

    # 사용자 id, 사용자 name 추출 후 dict형식 변환
    user_data = { "userid" : user_result.user_id, "username" : user_result.user_name }

    # StorageList 테이블에서 변수userid가 참여한 TeamStorage 이름 추출
    # sql : select team_storage from storagelist where user_id = 변수userid;
    ts_result = StorageList.objects.filter(user_id = userid).values("team_storage")

    # list 선언 ( 배열 )
    ts_data = []

    # select 결과값만 list로 변환
    for temp in ts_result:
        ts_data.append(temp['team_storage'])

    # user_data, ts_data 통합
    data = { "user" : user_data, "storage" : ts_data }
    
    # Json 형식으로 data 반환
    return JsonResponse(data)

# http://localhost:8000/profile
# profile 페이지 실행 함수
def profile(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # User 테이블에서 Primary key가 userid인 레코드 호출
    # sql : select * from user where primary key = 변수userid;
    user_result = User.objects.get(pk = userid)

    # 사용자가 생성한 페이지 리스트 호출
    # sql : select storage_name from teamstorage where master_id = 변수userid;
    ts_master_result = TeamStorage.objects.filter(master_id = userid).values("storage_name")

    # list 선언 ( 배열 )
    ts_master_data = []

    # select 결과값만 list로 변환
    for temp in ts_master_result:
        ts_master_data.append(temp['storage_name'])

    # Profile.html 반환 시 유저id, 유저이름, 유저전화번호와 자신이 생성한 TeamStorage List 반환
    return render(request, 'Profile.html', { "userid" : user_result.user_id, "username" : user_result.user_name, "userphone" : user_result.user_phone, 'data' : ts_master_data })

# http://localhost:8000/sign_in
# Sign in 페이지 실행 함수 및 회원가입 수행 함수
def sign_in(request):
    # Post 요청 시 실행
    if request.method == "POST":
        # Post 형식 데이터 data변수에 저장
        data = request.POST;

        # User 테이블에 회원정보 등록
        # insert into user values(data['userid'], data['userpw'], data['username'], data['userphone']);
        User.objects.create(user_id = data['userid'], user_pw = data['userpw'], user_name = data['username'], user_phone = data['userphone'])

        # data 내부 personal 저장 공간으로 이동
        os.chdir("../data/personal")

        # 개인 이름 저장 공간 생성
        os.makedirs(data['userid'])

        # 웹 서버 경로로 이동
        os.chdir(position)

        # urls.py에 path 중 이름 login 호출
        return redirect('login')
    
    # Post 형식 데이터가 없을 시 Sign_in.html 반환
    return render(request, 'Sign_in.html')

# http://localhost:8000/find_id_reset_pw
# 아이디 찾기 및 비밀번호 재설정 페이지 호출 함수
def find_id_reset_pw(request):
    # Find_ID_Reset_PW.html 반환
    return render(request, 'Find_ID_Reset_PW.html')

# 로그아웃 수행 함수
def logout(request):
    # 세션에 존재하는 userid 삭제
    request.session.pop('userid')

    # urls.py에 path 중 이름 login 호출
    return redirect('login')

# TeamStorage 이동 함수
def movetots(request):
    # Get 형식으로 넘어오는 TeamStorage 이름을 storage_name에 저장
    storage_name = request.GET['name']

    # storage_name의 값을 ts_name으로 세션 추가
    request.session['ts_name'] = storage_name
    
    # urls.py에 path 중 이름 team_storage 호출
    return redirect('team_storage')

# 비밀번호 재설정 페이지 이동 함수
def movetoresetpw(request):
    # 세션에 존재하는 userid 삭제
    request.session.pop('userid')

    # urls.py에 path 중 이름 find_id_reset_pw 호출
    return redirect('find_id_reset_pw')

# TeamStroage Master 페이지 이동 함수
def movetotsmaster(request):
    # Get 형식으로 넘어오는 TeamStorage 이름을 storage_name에 저장
    storage_name = request.GET['ts_name']

    # storage_name의 값을 ts_name으로 세션 추가
    request.session['ts_name'] = storage_name

    # urls.py에 path 중 이름 ts_master 호출
    return redirect('ts_master')