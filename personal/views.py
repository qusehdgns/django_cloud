# 웹 url 호출 시 html 및 템플릿 변수 전송
from django.shortcuts import render
# 웹 url 호출 시 다른 url로 이동
from django.shortcuts import redirect
# 웹에 문자열 리턴
from django.http import HttpResponse
# Json 형식의 데이터 리턴
from django.http import JsonResponse
# Post 통신 시 필요한 암호화를 우회
from django.views.decorators.csrf import csrf_exempt

# 파일 과련 함수 사용
import os
# 디렉토리 관련 함수
import shutil
# Json 형식 사용
import json

# 데이터 베이스 연동 기능
# personal App의 models.py 내부 class 선언
from personal.models import  PSInfo, setdir

# personal App에 forms.py 내부 PSInfoForm
from personal.forms import PSInfoForm

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
    try:
        userid = request.session['userid']
    except KeyError:
        return render(request, "login.html")
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
    
    # GET 방식 데이터가 없을 경우(사용자 최상위 폴더)
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

    # folder 리스트
    folder_list = []

    # file 리스트
    files_list = []

    # PSInfo 데이터베이스를 호출해서 psinfo 변수에 저장
    psinfo = PSInfo.objects

    # psinfo 정보 중 해당 파일 경로 내부에 파일이 있는지 확인
    # __startswith 문자열 시작부분 검색 기능
    if psinfo.filter(file__startswith = dirpath).exists() == True:
        # 내부에 파일이 있을 경우 해당 경로 내부 파일들 정보를 psinfo 변수에 저장 
        psinfo = psinfo.filter(file__startswith = dirpath).order_by('filename')

        # 사용자 내부 디렉토리 목록을 각각 불러와서 temp 변수에 저장
        for temp in file_list:

            # 내부 정보 데이터베이스에서 파일의 경로를 검색하여 주석 및 메모 레코드를 호출
            descript = psinfo.filter(file = dirpath + "/" + temp).values("descript", 'file')

            # data 변수에 dict 형식으로 파일 이름과 불러온 주석 및 메모를 저장
            data = { "filename" : temp, "descript" : descript[0]["descript"], "file" : descript[0]['file'] }

            if '.' in temp:
                files_list.append(data)

            else:
                folder_list.append(data)
    
    data_list.extend(folder_list)

    data_list.extend(files_list)
            
    # 웹 서버 경로로 이동
    os.chdir(position)

    # 사용자에게 보여줄 폴더 경로 문자열 변환 후 분할
    show_root = dirpath.replace("personal/" + userid, "Home", 1).split("/")

    # Personal_Storage.html 반환 시 상위폴더 존재 여부, 사용자id, 사용자 저장공간 내부 파일 리스트 반환
    return render(request, 'Personal_Storage.html', { 'folder' : pos ,'userid' : userid, 'data' : data_list, 'root' : enumerate(show_root), "index" : len(show_root)-1 })

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

# File Upload 관련 함수
@csrf_exempt
def personal_file_upload(request):
    # 세션에 존재하는 디렉토리 경로를 불러와 dirpath 변수에 저장    
    dirpath = request.session['dirpath']

    # 세션에 현재 디렉토리 정보(dir)가 세션에 존재하는지 확인
    if request.session.has_key('dir'):
        # 존재할 시 dirpath 정보 값을 기존 정보와 dir 세션 정보 통합
        dirpath = dirpath + "/" + request.session['dir']
    
    # Personal App에 models.py에 존재하는 데이터베이스 디렉토리 경로 설정 함수
    setdir(dirpath)

    # PSInfo 데이터베이스 변수 psinfo에 저장
    psinfo = PSInfo.objects

    # 파일명 변수 filename에 저장
    filename = request.POST['filename']

    # 공백을 _문자로 치환
    temp = filename.replace(" ", "_")

    # Personal Storage에 해당 파일 존재 확인
    if psinfo.filter(file = dirpath + "/" + temp).exists() == True:
        # 중복 파일 이 존재한다면 DB값 삭제
        psinfo.filter(file = dirpath + "/" + temp).delete()

        # 상위 폴더 이동
        os.chdir("..")

        # data 디렉토리로 이동
        os.chdir("./data")

        # 파일이면 해당 파일만 삭제
        os.remove("./" + dirpath + "/" + temp)

        # 웹 서버 경로로 이동
        os.chdir(position)

    # Post형식으로 넘어온 파일과 해당 정보들을 form에 지정한 형식에 저장하여 form 변수에 저장
    form = PSInfoForm(request.POST, request.FILES)

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
def psdeletefile(request):
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
    psinfo = PSInfo.objects

    # 파일 및 디렉토리 삭제 함수
    for temp in filename['array']:
        # 파일인지 확인
        if "." in temp:
            # 파일이면 해당 파일만 삭제
            os.remove("./" + dirpath + "/" + temp)

            # Personal Storage 데이터베이스 정보 삭제(해당 파일만 삭제)
            psinfo.filter(file = dirpath + "/" + temp).delete()
        else:
            # 디렉토리면 내부까지 전부 삭제
            shutil.rmtree("./" + dirpath + "/" + temp)
            # Personal Storage 데이터베이스 정보 삭제(디렉토리 경로 포함 전부 삭제)
            psinfo.filter(file__startswith = dirpath + "/" + temp).delete()

    # 웹 서버 경로로 이동
    os.chdir(position)

    # 삭제 완료 의미 "success" 리턴
    return HttpResponse("success")


@csrf_exempt
def psfilecheck(request):
    # 상위 디렉토리 경로 호출
    dirpath = request.session['dirpath']    

    # 상위 폴더 이동
    os.chdir("..")

    # data 디렉토리로 이동
    os.chdir("./data")

    # POST 방식 데이터 수신
    data = request.POST['filenames']

    # 수신된 문자열 형식 json을 dict 형식으로 변환
    filename = json.loads(data)

    # 세션에 dir 세션이 존재하는 지 확인
    if request.session.has_key('dir'):
        # 세션에 dir이 존재할 시 dirpath 세션에 dir 세션을 통합하여 저장
        dirpath = dirpath + "/" + request.session["dir"]

    # 현재 경로로 이동
    os.chdir("./" + dirpath)

    # 중복 파일 이름 담을 list 생성
    file_name = [];

    # 파일 및 디렉토리 내부 압축
    for i, temp in enumerate(filename['array']):
        # 공백을 _문자로 치환
        temp = temp.replace(" ", "_")

        # 중복 파일 존재 확인
        if os.path.exists(temp):
            # 존재한다면 파일 카운트 1 증가
            file_name.append(filename['array'][i])
    
    # 웹 서버 경로로 이동
    os.chdir(position)

    result = { "array" : file_name }

    # 중복 파일 개수 리턴
    return JsonResponse(result)