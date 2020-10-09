from django.shortcuts import render

import os

# main App의 models.py 내부 class 선언
from main.models import StorageList

# data 디렉토리 경로
data_location = "C:/Users/quseh/Desktop/workspace/django/Capstone/data"

# 웹 서버 경로
web_location = "C:/Users/quseh/Desktop/workspace/django/Capstone/cloud"

# http://localhost:8000/team/
# TeamStorage 페이지 호출 함수
def team_storage(request):
    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # data 내부 team 저장 공간으로 이동
    os.chdir(data_location + "/team")

    # 선택 team storage 디렉토리 이동
    os.chdir("./" + ts_name)

    # 사용자 내부 디렉터리 목록 저장
    file_list = os.listdir("./")

    # 웹 서버 경로로 이동
    os.chdir(web_location)

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
    # TS_File_Upload.html 반환
    return render(request, "TS_File_Upload.html")