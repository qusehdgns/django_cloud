from django.shortcuts import render
from django.http import HttpResponse

# directory 관련
import os

# json
import json

# Create your views here.
def test(request):

    # 초기 디렉터리 저장
    position = os.getcwd()

    # 상위 디렉터리 이동
    os.chdir("..")

    # data 디렉터리 확인 후 없을 시 생성
    if not os.path.exists("data"):
        os.makedirs("data")

    # 초기 디렉터리로 이동
    os.chdir(position)

    return render(request, 'test.html')

# makefolder 실행 함수
def makefolder(request):
    return render(request, 'makefolder.html')

def makefolderaction(request):
    # GET 방식 name 추출
    name = request.GET['name']

    # 초기 디렉터리 저장
    position = os.getcwd()

    # 상위 디렉터리 이동
    os.chdir("..")

    # data 디렉터리 이동
    os.chdir("./data")

    # data 디렉터리 확인 후 없을 시 생성
    if not os.path.exists(name):
        os.makedirs(name)
    else :
        return HttpResponse("error")
    
    # 초기 디렉터리로 이동
    os.chdir(position)

    return HttpResponse(name)
    

# listfolder 실행 함수
# 디렉토리 내부 리스트를 불러옴
def listfolder(request):

    # 초기 디렉터리 저장
    position = os.getcwd()

    # 상위 디렉터리 이동
    os.chdir("..")

    # data 디렉터리 이동
    os.chdir("./data")

    # data 내부 디렉터리 목록 저장
    folder_list = os.listdir("./")

    # 초기 디렉터리로 이동
    os.chdir(position)

    return render(request, 'listfolder.html', { 'list' : folder_list })


# 파일 삭제 함수
def deletefolder(request):

    # GET 방식 name 추출
    data = request.GET['list']

    # 문자열 json 변환
    folder_list = json.loads(data)

    # 초기 디렉터리 저장
    position = os.getcwd()

    # 상위 디렉터리 이동
    os.chdir("..")

    # data 디렉터리 이동
    os.chdir("./data")

    for folder in folder_list:
        os.rmdir('./' + folder)
    
    # 초기 디렉터리로 이동
    os.chdir(position)

    return HttpResponse(len(folder_list))