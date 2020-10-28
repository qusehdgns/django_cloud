# 웹 url 호출 시 html 및 템플릿 변수 전송
from django.shortcuts import render
# 웹 url 호출 시 다른 url로 이동
from django.shortcuts import redirect
# 웹에 문자열 리턴
from django.http import HttpResponse

# main App의 models.py 내부 class 선언
from main.models import User, StorageList
# master App의 models.py 내부 class 선언
from master.models import TeamStorage
# team App의 models.py 내부 class 선언
from team.models import Notice

# 시간 형식 변환
import datetime

# http://localhost:8000/master/
# TeamStorage Master 페이지 이동 함수
def ts_master(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # StorageList 내부에서 선택 teamstorage의 사용자 ID, 권한 호출
    # sql : select user_id, personal_auth from storagelist where team_storage = 변수ts_name;
    user_result = StorageList.objects.filter(team_storage = ts_name).values("user_id", "personal_auth")

    # list 선언 ( 배열 )
    user_data = []

    # select 결과값만 list로 변환
    for temp in user_result:
        user = { 'userid' : temp['user_id'], 'auth' : temp['personal_auth']}
        user_data.append(user)

    # 해당 TeamStorage 게시물 정보 추출 후 날짜 순으로 정렬
    notice = Notice.objects.filter(team_storage = ts_name).values('title', 'input_time').order_by('input_time')

    # list 선언 ( 배열 )
    notice_data = []

    # 추출 결과값을 dict 배열로 변환
    for temp in notice:
        notice_temp = { 'title' : temp['title'], 'input_time' : temp['input_time']}
        notice_data.append(notice_temp)

    # TS_Master.html 반환 시 TeamStorage이름, 유저ID, TeamStorage 사용자 정보 반환
    return render(request, "TS_Master.html", { 'ts_name' : ts_name, 'userid' : userid, 'data' : user_data, 'notice' : notice_data })

# http://localhost:8000/master/ts_notice_upload
# 공지사항 작성 페이지 호출
def ts_notice_upload(request):
    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # 세션에서 userid 호출
    userid = request.session['userid']
    
    # POST 형식 확인
    if request.method == "POST":
        # POST 형식 데이터를 data 변수에 저장
        data = request.POST

        # User 데이터베이스에서 선택 user 정보 레코드 추출
        user = User.objects.get(pk = userid)

        # TeamStorage 데이터베이스에서 선택 TeamStorage 정보 레코드 추출
        teamstorage = TeamStorage.objects.get(pk = ts_name)

        # Team Notice 데이터베이스에 게시물 정보 추가
        Notice.objects.create(team_storage=teamstorage, author=user, title=data['title'], value=data['value'])

        # Master 페이지로 페이지 이동
        return redirect('ts_master')

    # TS_Master.html 반환 시 TeamStorage이름 반환
    return render(request, "TS_Notice_Upload.html", { 'ts_name' : ts_name })

# Team Notice 중복 확인 함수
def notice_check(request):
    # GET 방식으로 넘어온 게시글 제목을 title 변수에 저장
    title = request.GET['title']
    
    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # 중복하는 제목의 게시물이 존재할 경우
    if Notice.objects.filter(team_storage=ts_name, title=title).exists() == True:
        # return 값은 'false"
        return HttpResponse('false')

    # 중복 게시물이 존재하지 않을 경우
    return HttpResponse('true')

# http://localhost:8000/master/ts_notice_update?title=타이틀
# Team Notice 수정 페이지
def ts_notice_update(request):
    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # 요청 형식이 POST인 경우
    if request.method == "POST":
        # POST 형식 data 변수에 저장
        data = request.POST

        # Team Notice 데이터베이스에서 사용자 선택 게시물의 레코드 호출
        notice = Notice.objects.filter(team_storage=ts_name, title=data['title'])

        # 데이터베이스 수정
        notice.update(value=data['value'], input_time=datetime.datetime.now())

        # ts_master 페이지로 이동
        return redirect('ts_master')
    
    # 요청 형식이 GET인 경우 data 변수에 저장
    data = request.GET

    # GET 방식 데이터에서 title을 변수 title에 저장
    title = data['title']

    # Team Notice 데이터베이스에서 사용자 선택 게시물의 레코드 호출
    notice = Notice.objects.filter(team_storage=ts_name, title=title).values('title', 'value')

    # 레코드 슬라이싱
    for temp in notice:
        notice = temp
    
    # 기존 게시물 정보와 TS_Notice_Update.html 리턴
    return render(request, "TS_Notice_Update.html", { 'data' : notice })