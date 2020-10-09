from django.shortcuts import render

import os

# data 디렉토리 경로
data_location = "C:/Users/quseh/Desktop/workspace/django/Capstone/data"

# 웹 서버 경로
web_location = "C:/Users/quseh/Desktop/workspace/django/Capstone/cloud"

# http://localhost:8000/personal/
# 개인 저장 공간 페이지 실행 함수
def personal_storage(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # data 내부 personal 저장 공간으로 이동
    os.chdir(data_location + "/personal")

    # 사용자 personal 디렉토리 이동
    os.chdir("./" + userid)

    # 사용자 내부 디렉터리 목록 저장
    file_list = os.listdir("./")

    # 웹 서버 경로로 이동
    os.chdir(web_location)

    # Personal_Storage.html 반환 시 사용자id, 사용자 저장공간 내부 파일 리스트 반환
    return render(request, 'Personal_Storage.html', { 'userid' : userid, 'data' : file_list })

# 개인 공간 파일 업로드 페이지 실행 함수
def ps_file_upload(request):
    # PS_File_Upload.html 반환
    return render(request, 'PS_File_Upload.html')