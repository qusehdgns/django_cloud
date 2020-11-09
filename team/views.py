# 웹 url 호출 시 html 및 템플릿 변수 전송
from django.shortcuts import render
# 웹 url 호출 시 다른 url로 이동
from django.shortcuts import redirect
# 웹에 문자열 리턴
from django.http import HttpResponse
# Post 통신 시 필요한 암호화를 우회
from django.views.decorators.csrf import csrf_exempt

# 파일 과련 함수 사용
import os
# 디렉토리 관련 함수
import shutil
# Json 형식 사용
import json

# 데이터 베이스 연동 기능
# main App의 models.py 내부 class 선언
from main.models import User, StorageList
# master App의 models.py 내부 class 선언
from master.models import TeamStorage
# team App의 models.py 내부 class 선언
from team.models import TSInfo, Notice, setdir

# team App에 forms.py 내부 TSInfoForm
from team.forms import TSInfoForm

# 시간 형식 변환
import datetime

# data 디렉토리 경로
data_location = "C:/Users/quseh/Desktop/workspace/django/Capstone/data"

# 웹 서버 경로
web_location = "C:/Users/quseh/Desktop/workspace/django/Capstone/cloud"

# 초기 디렉터리 저장
position = os.getcwd()

# http://localhost:8000/team/
# TeamStorage 페이지 호출 함수
def team_storage(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # GET 방식 통신인지 확인
    if request.GET:
        # GET 방식에서 전해져 온 선택 디렉토리(dir)를 dir 세션에 저장
        request.session["dir"] = request.GET['dir']
        
        # 세션에서 dirpath(디렉토리 경로) 세션을 dirpath 변수에 저장
        dirpath = request.session['dirpath']

        # dirpath 변수에 기존 dirpath와 dir 세션값을 통합하여 dirpath에 저장
        # 현재 보려고 하는 디렉토리 경로
        dirpath = dirpath + "/" + request.session['dir']

        # 하위 폴더라는 정보의 'non-top'을 저장
        pos = "non-top"
    
    # GET 방식 통신이 아닐 경우(사용자 최상위 폴더)
    else:
        # 세션에 dir 세션이 존재할 경우
        if request.session.has_key('dir'):
            # 세션에서 dir 세션을 지움
            request.session.pop('dir')

        # dir 경로를 최상위로 설정(../data/team/ts_name)
        dirpath = "team/" + ts_name

        # 최상위 폴더라는 정보의 'top'을 저장
        pos = "top" 

        # dirpath 정보를 dirpath 세션에 저장
        request.session['dirpath'] = dirpath

    # data 내부 personal 저장 공간으로 이동
    os.chdir("../data/" + dirpath)

    # 사용자 내부 디렉터리 목록 저장
    file_list = os.listdir("./")

    # 폴더 내부 정보를 담을 list 선언
    data_list = []

    # TSInfo 데이터베이스를 호출해서 tsinfo 변수에 저장
    tsinfo = TSInfo.objects

    # StorageList 데이터베이스에서 선택 TeamStorage의 사용자 권한 레코드 호출
    user_auth = StorageList.objects.filter(user_id = userid, team_storage = ts_name).values("personal_auth")

    # 호출 레코드 내부에서 사용자 권한 추출
    user_auth = user_auth[0]["personal_auth"]

    # TeamStorage 데이터베이스에서 선택 TeamStorage 정보 레코드 추출
    team = TeamStorage.objects.get(pk = ts_name)

    # 호출 레코드 내부에서 TeamStorage 권한 추출
    team_auth = team.authority

    # 호출 레코드 내부에서 TeamStorage 설명 추출
    team_descript = team.description

    # tsinfo 정보 중 해당 파일 경로 내부에 파일이 있는지 확인
    # __startswith 문자열 시작부분 검색 기능
    if tsinfo.filter(file__startswith = dirpath).exists() == True:
        # 내부에 파일이 있을 경우 해당 경로 내부 파일들 정보를 psinfo 변수에 저장 
        tsinfo = tsinfo.filter(file__startswith = dirpath)

        # Team Storage 사용 계급이 0일 경우
        if team_auth == 1:
            for temp in file_list:
                # 내부 정보 데이터베이스에서 파일의 경로를 검색하여 레코드를 호출
                data_temp = tsinfo.filter(file = dirpath + "/" + temp).values()

                # data 변수에 dict 형식으로 파일 이름과 불러온 주석 및 메모를 저장
                data = { "filename" : temp, "descript" : data_temp[0]["descript"] }

                # data_list 변수(list)에 추가
                data_list.append(data)
        else:
            # 사용자 내부 디렉토리 목록을 각각 불러와서 temp 변수에 저장
            for temp in file_list:
                # 내부 정보 데이터베이스에서 파일의 경로를 검색하여 레코드를 호출
                data_temp = tsinfo.filter(file = dirpath + "/" + temp).values()

                # 사용자 권한과 파일 권한 비교
                if user_auth <= data_temp[0]["access_auth"]:
                    # 사용자 권한이 파일 권한보다 작을 경우
                    # data 변수에 dict 형식으로 파일 이름과 불러온 주석 및 메모를 저장
                    data = { "filename" : temp, "descript" : data_temp[0]["descript"] }

                    # data_list 변수(list)에 추가
                    data_list.append(data)
            
    # 웹 서버 경로로 이동
    os.chdir(position) 

    # 해당 TeamStorage 게시물 정보 추출 후 날짜 순으로 정렬
    notice = Notice.objects.filter(team_storage = ts_name).values('title', 'input_time').order_by('input_time')

    # list 선언 ( 배열 )
    notice_data = []

    # 추출 결과값을 dict 배열로 변환
    for temp in notice:
        notice_temp = { 'title' : temp['title'], 'input_time' : temp['input_time']}
        notice_data.append(notice_temp)

    # Team_Storage.html 반환 시 상위폴더 존재 ㅣ여부, TeamStroage이름, TeamStorage 내부 파일 리스트, 사용자 권한, Team Storage 계급 반환
    return render(request, "Team_Storage.html",
        { 'folder' : pos, 'name' : ts_name, 'data' : data_list, "user_auth" : user_auth, "team_auth" : team_auth,
        'team_descript' : team_descript, 'notice' : notice_data, "range" : range(1, team_auth+1) })

# Team Storage 디렉토리 내부에 폴더 생성 시 실행 함수
def tsaddfolder(request):
    # 사용자가 요청한 GET 방식 내부 folder 이름을 folder_name 변수에 저장
    folder_name = request.GET['folder_name']

    # 폴더에 저장할 descript(주석 및 설명)을 GET 방식 내부에서 받아 descript 변수에 저장
    descript = request.GET['descript']

    auth = request.GET['auth']

    # descript 공백 확인
    if descript == "":
        # 공백일 경우 None 값으로 변환
        descript = None

    # 세션에서 현재 디렉토리 경로 정보를 dirpath 변수에 저장
    dirpath = request.session['dirpath']

    # 세션에 현재 디렉토리 정보(dir)가 세션에 존재하는지 확인
    if request.session.has_key('dir'):
        # 존재할 시 dirpath 정보 값을 기존 정보와 dir 세션 정보 통합
        dirpath = dirpath + "/" + request.session['dir']

    # 현재 접속 디렉토리를 ../data/ + dirpath 경로로 이동
    os.chdir("../data/" + dirpath)

    # 해당 경로에 folder_name 값의 폴더 생성
    os.makedirs(folder_name)

    # PSInfo에 폴더 이름, 폴더 경로, 해당 폴더 설명, 접근 권한을 생성
    TSInfo.objects.create(filename = folder_name, file = dirpath + "/" + folder_name, descript = descript, access_auth = auth)

    # 초기 웹 서버 디렉토리로 이동
    os.chdir(position)

    # 생성 완료문(String) 리턴
    return HttpResponse("폴더를 생성하였습니다.")

# 내부 폴더 이동 시 세션값 설정
def tsmovefolder(request):
    # 세션에 dir 세션이 존재하는 지 확인
    if request.session.has_key('dir'):
        # 세션에 dir이 존재할 시 dirpath 세션에 dir 세션을 통합하여 저장
        request.session['dirpath'] = request.session['dirpath'] + "/" + request.session["dir"]
    
    # 웹 url을 /personal/?dir= + dir 경로로 전환
    return redirect("/team/?dir=" + request.GET['dir'])

# http://localhost:8000/team/team_storage_list
def team_storage_list(request):

    # 세션에서 userid 호출
    userid = request.session['userid']

    # 사용자가 사용하고 있는 TeamStorage 이름 호출
    # sql : select team_storage from storagelist where user_id = 변수userid;
    ts_result = StorageList.objects.filter(user_id = userid).values("team_storage")

    # list 선언 ( 배열 )
    ts_data = []

    # TeamStorage 데이터베이스 teamstorage 변수에 저장
    teamstorage = TeamStorage.objects;

    # select 결과값만 list로 변환 및 본인 Team Storage 식별
    for temp in ts_result:
        # 검색한 Team Storage 이름이 본인이 만든 Team Storage 이름인지 식별
        if teamstorage.filter(storage_name = temp['team_storage'], master_id = userid).exists() == True:
            data = { "storage_name" : temp['team_storage'], "master" : "Master" }

        # 검색한 Team Storage가 본인이 만든 것이 아닐 경우
        else:
            # Team Storage 이름만 추가
            data = { "storage_name" : temp['team_storage'] }

        ts_data.append(data)

    # Team_Storage_List.html 반환 시 사용자가 접속한 TeamStorage 리스트 반환
    return render(request, "Team_Storage_List.html", { "data" : ts_data })

# http://localhost:8000/team/team_storage_create
# TeamStorage 생성 페이지 호출 함수
def team_storage_create(request):
    # Team_Storage_Create.html 반환
    return render(request, "Team_Storage_Create.html")

# http://localhost:8000/team/ts_file_upload
# TeamStorage 파일 업로드 페이지 호출 함수
def ts_file_upload(request):
    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # 업로드 완료 후 기존 경로로 돌아가기 위한 url을 GET 방식을 받아 url 변수에 저장
    url = request.GET['url']

    # TeamStorage 데이터베이스에서 선택 TeamStorage 정보 레코드 추출
    team = TeamStorage.objects.get(pk = ts_name)

    # 호출 레코드 내부에서 TeamStorage 권한 추출
    team_auth = team.authority

    # 돌아가기 위한 url 정보를 담아 TS_File_Upload.html 반환
    return render(request, "TS_File_Upload.html",{ "url" : url, "team_auth" : team_auth, "range" : range(1, team_auth+1) })

# File Upload 관련 함수
@csrf_exempt
def team_file_upload(request):
    # 세션에 존재하는 디렉토리 경로를 불러와 dirpath 변수에 저장    
    dirpath = request.session['dirpath']

    # 세션에 현재 디렉토리 정보(dir)가 세션에 존재하는지 확인
    if request.session.has_key('dir'):
        # 존재할 시 dirpath 정보 값을 기존 정보와 dir 세션 정보 통합
        dirpath = dirpath + "/" + request.session['dir']
    
    # Team App에 models.py에 존재하는 데이터베이스 디렉토리 경로 설정 함수
    setdir(dirpath)

    # Post형식으로 넘어온 파일과 해당 정보들을 form에 지정한 형식에 저장하여 form 변수에 저장
    form = TSInfoForm(request.POST, request.FILES)

    # form 형식 유효성(validation) 확인
    if form.is_valid():
        # form 형식에 이상이 없을 시 저장 및 데이터베이스 적용
        form.save()
        # 저장 성공 시 'success' 리턴
        return HttpResponse("success")
    else:
        # validation(유효성) 오류 발생 시 해당 항목 console에 출력
        print(form.errors)
    
    # 유효성 검사 실패 시 'fail' 리턴
    return HttpResponse("fail")

# 파일 삭제 함수
@csrf_exempt
def tsdeletefile(request):
    # POST 방식 데이터 수신
    data = request.POST['filename']

    # 수신된 문자열 형식 json을 dict 형식으로 변환
    filename = json.loads(data)

    # 상위 디렉토리 경로 호출
    dirpath = request.session['dirpath']

    # 세션에 dir 세션이 존재하는 지 확인
    if request.session.has_key('dir'):
        # 세션에 dir이 존재할 시 dirpath 세션에 dir 세션을 통합하여 저장
        dirpath = dirpath + "/" + request.session["dir"]
    
    # 상위 폴더 이동
    os.chdir("..")

    # data 디렉토리로 이동
    os.chdir("./data")

    # PSInfo 데이터베이스를 호출해서 psinfo 변수에 저장
    tsinfo = TSInfo.objects

    # 파일 및 디렉토리 삭제 함수
    for temp in filename['array']:
        # 파일인지 확인
        if "." in temp:
            # 파일이면 해당 파일만 삭제
            os.remove("./" + dirpath + "/" + temp)

            # Personal Storage 데이터베이스 정보 삭제(해당 파일만 삭제)
            tsinfo.filter(file = dirpath + "/" + temp).delete()
        else:
            # 디렉토리면 내부까지 전부 삭제
            shutil.rmtree("./" + dirpath + "/" + temp)
            # Personal Storage 데이터베이스 정보 삭제(디렉토리 경로 포함 전부 삭제)
            tsinfo.filter(file__startswith = dirpath + "/" + temp).delete()

    # 웹 서버 경로로 이동
    os.chdir(position)

    # 삭제 완료 의미 "success" 리턴
    return HttpResponse("success")

# Team Storage 생성 시 Team Storage 이름 확인 함수
def tsnamecheck(request):

    # Team Storage 데이터베이스에서 사용자가 요청한 TeamStorage 이름이 존재하는지 확인
    if TeamStorage.objects.filter(storage_name = request.GET["ts_name"]).exists() == True :
        # Team Storage 이름이 존재할 경우 사용 불가의 'false' 리턴
        return HttpResponse("false")

    # Team Storage 이름이 존재하지 않아 사용  가능할 경우 'true' 리턴
    return HttpResponse("true")

# Team Storage 생성 함수
def createteamstorage(request):

    # 세션에서 userid 호출
    userid = request.session['userid']

    # 외래키의 저장을 위해 데이터베이스 레코드 저장
    # User 데이터베이스에서 사용자 id를 검색하여 user_id 변수에 저장
    user_id = User.objects.get(pk = userid)

    # GET 방식으로 들어온 데이터를 data 변수에 저장
    data = request.GET

    # Team Storage 데이터베이스에 사용자가 요청한 Team Storage 이름, 설명, 권한, Master ID를 저장
    TeamStorage.objects.create(storage_name=data["ts_name"], description=data["ts_descript"], authority=data["ts_auth"], master_id=user_id)

    # 외래키의 저장을 위해 데이터베이스 레코드 저장
    # Team Storage 데이터베이스에서 생성 요청한 Team Storage 이름을 검색하여 ts_name 변수에 저장
    ts_name = TeamStorage.objects.get(pk = data["ts_name"])

    # StorageList 데이터베이스에 사용자 id, Team Storage 이름, 권한(Master 권한 = 0) 저장
    StorageList.objects.create(user_id=user_id, team_storage=ts_name, personal_auth=0)

    # data 내부 team 저장 공간으로 이동
    os.chdir("../data/team")

    # 스토리지 이름 저장 공간 생성
    os.makedirs(data["ts_name"])

    # 웹 서버 경로로 이동
    os.chdir(position)

    # 웹으로 리턴
    return HttpResponse()

# http://localhost:8000/team/team_notice?title=제목&url=접속 url
# Team Notice 게시물 확인 페이지 호출 함수
def team_notice(request):
    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # GET 방식의 데이터 변수 data에 저장
    data = request.GET

    # 돌아갈 url 저장
    url = data['url']

    # Team Notice 데이터베이스에서 사용자 선택 게시물 정보 검색
    notice = Notice.objects.filter(team_storage = ts_name, title = data['title']).values()

    # filter 사용을 위한 슬라이싱
    for temp in notice:
        notice = temp

    # 사용할 데이터 dict 형식으로 변환
    notice_data = { "title" : notice['title'], "value" : notice['value'], "author" : notice['author_id'], "time" : notice['input_time'].strftime('%Y-%m-%d %H:%M:%S')}

    return render(request, "Team_Notice.html", { 'data' : notice_data, 'url' : url })