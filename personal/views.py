# 웹 url 호출 시 html 및 템플릿 변수 전송
from django.shortcuts import render
# 웹 url 호출 시 다른 url로 이동
from django.shortcuts import redirect
# 웹에 문자열 리턴
from django.http import HttpResponse

# 파일 과련 함수 사용
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

        # dir 경로를 최상위로 설정(../data/personal/userid)
        dirpath = "personal/" + userid

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

    # PSInfo 데이터베이스를 호출해서 psinfo 변수에 저장
    psinfo = PSInfo.objects

    # psinfo 정보 중 해당 파일 경로 내부에 파일이 있는지 확인
    # __startswith 문자열 시작부분 검색 기능
    if psinfo.filter(file__startswith = dirpath).exists() == True:
        # 내부에 파일이 있을 경우 해당 경로 내부 파일들 정보를 psinfo 변수에 저장 
        psinfo = psinfo.filter(file__startswith = dirpath)

        # 사용자 내부 디렉토리 목록을 각각 불러와서 temp 변수에 저장
        for temp in file_list:
            # 내부 정보 데이터베이스에서 파일의 경로를 검색하여 주석 및 메모 레코드를 호출
            descript = psinfo.filter(file = dirpath + "/" + temp).values("descript", 'file')

            # data 변수에 dict 형식으로 파일 이름과 불러온 주석 및 메모를 저장
            data = { "filename" : temp, "descript" : descript[0]["descript"], "file" : descript[0]['file'] }

            # data_list 변수(list)에 추가
            data_list.append(data)
            
    # 웹 서버 경로로 이동
    os.chdir(position)

    # Personal_Storage.html 반환 시 상위폴더 존재 여부, 사용자id, 사용자 저장공간 내부 파일 리스트 반환
    return render(request, 'Personal_Storage.html', { 'folder' : pos ,'userid' : userid, 'data' : data_list })

# Personal Storage 디렉토리 내부에 폴더 생성 시 실행 함수
def psaddfolder(request):
    # 사용자가 요청한 GET 방식 내부 folder 이름을 folder_name 변수에 저장
    folder_name = request.GET['folder_name']

    # 폴더에 저장할 descript(주석 및 설명)을 GET 방식 내부에서 받아 descript 변수에 저장
    descript = request.GET['descript']

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

    # PSInfo에 폴더 이름, 폴더 경로, 해당 폴더 설명을 생성
    PSInfo.objects.create(filename = folder_name, file = dirpath + "/" + folder_name, descript = descript)

    # 초기 웹 서버 디렉토리로 이동
    os.chdir(position)

    # 생성 완료문(String) 리턴
    return HttpResponse("폴더를 생성하였습니다.")

# 내부 폴더 이동 시 세션값 설정
def psmovefolder(request):
    # 세션에 dir 세션이 존재하는 지 확인
    if request.session.has_key('dir'):
        # 세션에 dir이 존재할 시 dirpath 세션에 dir 세션을 통합하여 저장
        request.session['dirpath'] = request.session['dirpath'] + "/" + request.session["dir"]
    
    # 웹 url을 /personal/?dir= + dir 경로로 전환
    return redirect("/personal/?dir=" + request.GET['dir'])

# 개인 공간 파일 업로드 페이지 실행 함수
def ps_file_upload(request):

    # 업로드 완료 후 기존 경로로 돌아가기 위한 url을 GET 방식을 받아 url 변수에 저장
    url = request.GET['url']

    # 돌아가기 위한 url 정보를 담아 PS_File_Upload.html 반환
    return render(request, 'PS_File_Upload.html',{ "url" : url })