from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse

import json

from main.models import User, StorageList

# Create your views here.
def login(request):
    # Post 형식 데이터가 들어오는지 확인
    if request.method == "POST":
        # Post 형식 데이터를 data 변수에 저장
        data = request.POST;

        # User 테이블에 사용자 id, pw 탐색
        if User.objects.filter(user_id = data['userid'], user_pw = data['userpw']).exists() == True :
            # 세션에 userid 담기
            request.session['userid'] = data['userid']

            # personal_storage 페이지로 이동
            return redirect('personal_storage')
        else:
            # 반환 html 문자열
            html = "<h1>로그인 실패</h1><input type='button' value='로그인 화면으로 이동' onclick='move();'></input>"
            html += "<script>function move(){location.href='/';}</script>"
            
            return HttpResponse(html)

    return render(request, 'Login.html')

def index(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # User 테이블에서 Primary key가 userid인 레코드 호출
    # sql : select * from user where primary key = 변수userid;
    user_result = User.objects.get(pk = userid)

    # 사용자 id, 사용자 name 추출 후 dict형식 변환
    user_data = { "userid" : user_result.user_id, "username" : user_result.user_name }

    # sql : select team_storage from storagelist where user_id = 변수userid;
    ts_result = StorageList.objects.filter(user_id = userid).values("team_storage")

    # list 선언 ( 배열 )
    ts_data = []

    # select 결과값만 list로 변환
    for temp in ts_result:
        ts_data.append(temp['team_storage'])

    # user_data, ts_data 통합
    data = { "user" : user_data, "storage" : ts_data }
    
    # Json 형식으로 반환
    return JsonResponse(data)

def profile(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # User 테이블에서 Primary key가 userid인 레코드 호출
    # sql : select * from user where primary key = 변수userid;
    user_result = User.objects.get(pk = userid)

    return render(request, 'Profile.html', { "userid" : user_result.user_id, "username" : user_result.user_name, "userphone" : user_result.user_phone })

def sign_in(request):
    # Post 요청 시 실행
    if request.method == "POST":
        data = request.POST;
        User.objects.create(user_id = data['userid'], user_pw = data['userpw'], user_name = data['username'], user_phone = data['userphone'])
        return redirect('login')
        
    return render(request, 'Sign_in.html')

def find_id_reset_pw(request):
    return render(request, 'Find_ID_Reset_PW.html')

def logout(request):
    request.session.pop('userid')
    return redirect('login')

def movetots(request):

    storage_name = request.GET['name']

    request.session['ts_name'] = storage_name
    
    return redirect('team_storage')

def movetoresetpw(request):
    request.session.pop('userid')
    return redirect('find_id_reset_pw')