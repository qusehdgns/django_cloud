# 웹 url 호출 시 html 및 템플릿 변수 전송
from django.shortcuts import render
# 웹에 문자열 리턴
from django.http import HttpResponse

# 파일 과련 함수 사용
import os

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

# http://localhost:8000/team/
# TeamStorage 페이지 호출 함수
def team_storage(request):
    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # data 내부 team 저장 공간으로 이동
    os.chdir("../data/team")

    # 선택 team storage 디렉토리 이동
    os.chdir("./" + ts_name)

    # 사용자 내부 디렉터리 목록 저장
    file_list = os.listdir("./")

    # 웹 서버 경로로 이동
    os.chdir(position)

    # Team_Storage.html 반환 시 TeamStroage이름, TeamStorage 내부 파일 리스트 반환
    return render(request, "Team_Storage.html", { 'name' : ts_name, 'data' : file_list })

# http://localhost:8000/team/team_storage_list
def team_storage_list(request):

    # 세션에서 userid 호출
    userid = request.session['userid']

    # 사용자가 사용하고 있는 TeamStorage 이름 호출
    # sql : select team_storage from storagelist where user_id = 변수userid;
    ts_result = StorageList.objects.filter(user_id = userid).values("team_storage")

    # list 선언 ( 배열 )
    ts_data = []

    # select 결과값만 list로 변환
    for temp in ts_result:
        ts_data.append(temp['team_storage'])

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

    # 업로드 완료 후 기존 경로로 돌아가기 위한 url을 GET 방식을 받아 url 변수에 저장
    url = request.GET['url']

    # 돌아가기 위한 url 정보를 담아 TS_File_Upload.html 반환
    return render(request, "TS_File_Upload.html",{ "url" : url })

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