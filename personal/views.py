from django.shortcuts import render

import os

# 데이터 베이스 연동 기능
# personal App의 models.py 내부 class 선언
from personal.models import  PSInfo

# data 디렉토리 경로
data_location = "C:/Users/quseh/Desktop/workspace/django/Capstone/data"

# 웹 서버 경로
web_location = "C:/Users/quseh/Desktop/workspace/django/Capstone/cloud"

# 초기 디렉터리 저장
position = os.getcwd()

# http://localhost:8000/personal/
# 개인 저장 공간 페이지 실행 함수
def personal_storage(request):
    # 세션에서 userid 호출
    userid = request.session['userid']
    
    if request.GET:
        request.session["dir"] = request.GET['dir']
        dirpath = request.session['dirpath']
        dirpath = dirpath + "/" + request.session['dir']
        pos = "non-top"
    else:
        if request.session.has_key('dir'):
            request.session.pop('dir')

        dirpath = "personal/" + userid
        pos = "top" 
        request.session['dirpath'] = dirpath


    # data 내부 personal 저장 공간으로 이동
    os.chdir("../data/" + dirpath)

    # 사용자 내부 디렉터리 목록 저장
    file_list = os.listdir("./")

    data_list = []

    psinfo = PSInfo.objects

    if psinfo.filter(file__startswith = dirpath).exists() == True:
        psinfo = psinfo.filter(file__startswith = dirpath)
        for temp in file_list:
            descript = psinfo.filter(file = dirpath + "/" + temp).values("descript")
            data = { "filename" : temp, "descript" : descript[0]["descript"] }
            data_list.append(data)
            
    # 웹 서버 경로로 이동
    os.chdir(position)

    # Personal_Storage.html 반환 시 사용자id, 사용자 저장공간 내부 파일 리스트 반환
    return render(request, 'Personal_Storage.html', { 'folder' : pos ,'userid' : userid, 'data' : data_list })

# 개인 공간 파일 업로드 페이지 실행 함수
def ps_file_upload(request):

    url = request.GET['url']

    # PS_File_Upload.html 반환
    return render(request, 'PS_File_Upload.html',{ "url" : url })