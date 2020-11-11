# 웹 url 호출 시 html 및 템플릿 변수 전송
from django.shortcuts import render
# 웹 url 호출 시 다른 url로 이동
from django.shortcuts import redirect
# 웹에 문자열 리턴
from django.http import HttpResponse
# Json 형식의 데이터 리턴
from django.http import JsonResponse
# 파일 정보 리턴
from django.http import FileResponse
# Post 통신 시 필요한 암호화를 우회
from django.views.decorators.csrf import csrf_exempt
# 데이터 저장 경로 확인(데이터 경로)
from cloud.settings import DATA_DIR

# Json 형식 사용
import json
# 파일 관련 함수 사용
import os
# zipping 관련 함수 사용
import zipfile
# 디렉토리 관련 함수
import shutil

# 데이터 베이스 연동 기능
# main App의 models.py 내부 class 선언
from main.models import User, StorageList
# master App의 models.py 내부 class 선언
from master.models import TeamStorage
# personal App의 models.py 내부 class 선언
from personal.models import  PSInfo
# team App의 models.py 내부 class 선언
from team.models import  TSInfo

# 초기 디렉터리 저장(웹 서버 경로)
position = os.getcwd()

# 초기 서버 디렉토리 생성 함수
def create_data_directory():
    # 상위 폴더 이동
    os.chdir("..")

    # data 디렉토리 없을 시 실행
    if not os.path.exists("data"):
        # data 디렉토리 생성
        os.makedirs("data")
    
    # data 디렉토리로 이동
    os.chdir("./data")

    # personal 디렉토리 없을 시 실행
    if not os.path.exists("personal"):
        # personal 디렉토리 생성
        os.makedirs("personal")

    # team 디렉토리 없을 시 실행
    if not os.path.exists("team"):
        # team 디렉토리 생성
        os.makedirs("team")
    
    # zip 디렉토리 없을 시 실행
    if not os.path.exists("zip"):
        # team 디렉토리 생성
        os.makedirs("zip")
    
    # 웹 서버 디렉토리로 이동
    os.chdir(position)

    return

# 초기 디렉토리 생성 실행
create_data_directory()

# http://localhost:8000/
# 초반 메인 Login 페이지 호출 및 로그인 수행 함수
def login(request):
    # 로그인 시에도 디렉토리 확인 및 생성
    create_data_directory()

    # Post 형식 데이터가 들어오는지 확인
    if request.method == "POST":
        # Post 형식 데이터를 data 변수에 저장
        data = request.POST;

        # User 테이블에 사용자 id, pw 탐색
        if User.objects.filter(user_id = data['userid'], user_pw = data['userpw']).exists() == True :
            # 세션에 userid 담기
            request.session['userid'] = data['userid']

            # urls.py에 path 중 이름 personal_storage 호출
            return redirect('personal_storage')
        else:
            # 반환 result 문자열
            result = "fail"

            # 문자열 자체를 반환
            return render(request, 'Login.html', { "result" : result })

    # Post 형식 데이터가 없을 시 Login.html 반환
    return render(request, 'Login.html')

# 사용자 정보를 표시하는 container html 함수 좌측 바를 담당
def index(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # User 테이블에서 Primary key가 userid인 레코드 호출
    # sql : select * from user where primary key = 변수userid;
    user_result = User.objects.get(pk = userid)

    # 사용자 id, 사용자 name 추출 후 dict형식 변환
    user_data = { "userid" : user_result.user_id, "username" : user_result.user_name, "useremo" : user_result.user_emo }

    # StorageList 테이블에서 변수userid가 참여한 TeamStorage 이름 추출
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

    # user_data, ts_data 통합
    data_list = { "user" : user_data, "storage" : ts_data }
    
    # Json 형식으로 data 반환
    return JsonResponse(data_list)

# http://localhost:8000/profile
# profile 페이지 실행 함수
def profile(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # User 테이블에서 Primary key가 userid인 레코드 호출
    # sql : select * from user where primary key = 변수userid;
    user_result = User.objects.get(pk = userid)

    # 사용자가 생성한 페이지 리스트 호출
    # sql : select storage_name from teamstorage where master_id = 변수userid;
    ts_master_result = TeamStorage.objects.filter(master_id = userid).values("storage_name")

    # list 선언 ( 배열 )
    ts_master_data = []

    # select 결과값만 list로 변환
    for temp in ts_master_result:
        ts_master_data.append(temp['storage_name'])

    # Profile.html 반환 시 유저id, 유저이름, 유저전화번호와 자신이 생성한 TeamStorage List 반환
    return render(request, 'Profile.html', { "userid" : user_result.user_id, "username" : user_result.user_name, "userphone" : user_result.user_phone, "useremo" : user_result.user_emo, 'data' : ts_master_data })

# http://localhost:8000/sign_in
# Sign in 페이지 실행 함수 및 회원가입 수행 함수
def sign_in(request):
    # Post 요청 시 실행
    if request.method == "POST":
        # Post 형식 데이터 data변수에 저장
        data = request.POST;

        # User 테이블에 회원정보 등록
        # insert into user values(data['userid'], data['userpw'], data['username'], data['userphone']);
        User.objects.create(user_id = data['userid'], user_pw = data['userpw'], user_name = data['username'], user_phone = data['userphone'])

        # data 내부 personal 저장 공간으로 이동
        os.chdir("../data/personal")

        # 개인 이름 저장 공간 생성
        os.makedirs(data['userid'])

        # 웹 서버 경로로 이동
        os.chdir(position)

        # urls.py에 path 중 이름 login 호출
        return redirect('login')
    
    # Post 형식 데이터가 없을 시 Sign_in.html 반환
    return render(request, 'Sign_in.html')

# 사용자 회원가입 시 사용자 id 중복 확인 함수
def idcheck(request):
    # 사용자가 사용할 ID가 User 데이터베이스에 존재하는지 확인
    if User.objects.filter(user_id = request.GET["userid"]).exists() == True :
        # 존재할 시 'false' 리턴
        return HttpResponse("false")

    # 사용 가능할 시 'true' 리턴
    return HttpResponse("true")

# http://localhost:8000/find_id_reset_pw
# 아이디 찾기 및 비밀번호 재설정 페이지 호출 함수
def find_id_reset_pw(request):
    # 세션에서 check값이 존재하는지 확인
    if request.session.has_key('check'):
        # 세션에 존재하는 check 삭제
        request.session.pop('check')

        return render(request, 'Find_ID_Reset_PW.html', { "check" : "know" })

    # Find_ID_Reset_PW.html 반환
    return render(request, 'Find_ID_Reset_PW.html')

# 로그아웃 수행 함수
def logout(request):
    # 세션에 존재하는 userid 삭제
    request.session.pop('userid')

    # urls.py에 path 중 이름 login 호출
    return redirect('login')

# TeamStorage 이동 함수
def movetots(request):
    # Get 형식으로 넘어오는 TeamStorage 이름을 storage_name에 저장
    storage_name = request.GET['name']

    # storage_name의 값을 ts_name으로 세션 추가
    request.session['ts_name'] = storage_name
    
    # urls.py에 path 중 이름 team_storage 호출
    return redirect('team_storage')

# 비밀번호 재설정 페이지 이동 함수
def movetoresetpw(request):
    # 로그인한 사용자의 비밀번호 재설정인지 판단하는 세션값
    request.session['check'] = "know"

    # 세션에 존재하는 userid 삭제
    request.session.pop('userid')

    # urls.py에 path 중 이름 find_id_reset_pw 호출
    return redirect('find_id_reset_pw')

# TeamStroage Master 페이지 이동 함수
def movetotsmaster(request):
    # Get 형식으로 넘어오는 TeamStorage 이름을 storage_name에 저장
    storage_name = request.GET['ts_name']

    # storage_name의 값을 ts_name으로 세션 추가
    request.session['ts_name'] = storage_name

    # urls.py에 path 중 이름 ts_master 호출
    return redirect('ts_master')

# 상위 폴더로 이동할 때 발생하는 세션 변경 함수
def uptofolder(request):
    # 세션에 존재하는 디렉토리 경로를 불러와 dirpath 변수에 저장    
    dirpath = request.session['dirpath']

    # 디렉토리 경로의 폴더 명들을 쪼개서 dir_root에 list 형식으로 저장
    dir_root = dirpath.split("/")

    # dir_root의 크기가 2보다 큰지 확인(사용자 최상위 폴더 식별)
    if len(dir_root) > 2:
        # 상위 폴더 이름을 value 변수에 저장
        value = dir_root[len(dir_root)-1]

        # dir_root[0] 변수에 나머지 경로들 통합하여 저장
        for i in range(len(dir_root) - 2):
            dir_root[0] = dir_root[0] +"/" + dir_root[i + 1]

        # dirpath 세션에 변환한 디렉토리 경로 저장
        request.session["dirpath"] = dir_root[0]

    # 최상위 폴더 일 경우
    else:
        # 최상위라 인식할 수 있는 top 문자열 value 변수에 저장
        value = "top"

    # value 정보를 리턴
    return HttpResponse(value)

# Profile 수정 함수
def changeprofile(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # GET 방식을 통한 데이터를 변수 data에 저장
    data = request.GET

    # User 데이터베이스에서 사용자 레코드 호출
    user = User.objects.filter(user_id=userid)

    # 데이터베이스 수정
    user.update(user_name=data['username'], user_phone=data['userphone'])

    # 프로필 변경 성공 "success" 리턴
    return HttpResponse("success")

# 파일 다운로드 함수
def download(request):
    # GET 방식 데이터 filename 수신
    filename = request.GET["filename"]

    # 상위 디렉토리 경로 호출
    dirpath = request.session['dirpath']

    # 세션에 dir 세션이 존재하는 지 확인
    if request.session.has_key('dir'):
        # 세션에 dir이 존재할 시 dirpath 세션에 dir 세션을 통합하여 저장
        dirpath = dirpath + "/" + request.session["dir"]

    # dirpath 시작 경로로 personal과 team을 구분
    if(dirpath.startswith("personal")):
        # personal일 경우 psinfo에 접근
        file_data = PSInfo.objects.get(file = dirpath + "/" + filename)
    else:
        # team일 경우 tsinfo에 접근
        file_data = TSInfo.objects.get(file = dirpath + "/" + filename)

    # 해당 파일 경로를 변수 file에 저장
    file = file_data.file.path

    # file을 통해 파일 정보 리턴
    return FileResponse(open(file, "rb"))

# Zipping 함수
@csrf_exempt
def zipping(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # 상위 디렉토리 경로 호출
    dirpath = request.session['dirpath']    

    # 상위 폴더 이동
    os.chdir("..")

    # data 디렉토리로 이동
    os.chdir("./data")

    # POST 방식 데이터 수신
    data = request.POST['filename']

    # 수신된 문자열 형식 json을 dict 형식으로 변환
    filename = json.loads(data)

    # 세션에 dir 세션이 존재하는 지 확인
    if request.session.has_key('dir'):
        # 세션에 dir이 존재할 시 dirpath 세션에 dir 세션을 통합하여 저장
        dirpath = dirpath + "/" + request.session["dir"]

    # zip 파일 생성
    zip_file = zipfile.ZipFile("./zip/" + userid + ".zip","w")

    # 현재 경로로 이동
    os.chdir("./" + dirpath)

    # 파일 및 디렉토리 내부 압축
    for temp in filename['array']:
        # 파일인지 확인
        if "." in temp:
            zip_file.write("./" + temp)
        else:
            # 내부 디렉토리까지 zipping
            for root, dirs, files in os.walk("./" + temp):
                for file in files:
                    zip_file.write(os.path.join(root, file))
    
    # zip 생성 완료
    zip_file.close()

    # 웹 서버 경로로 이동
    os.chdir(position)

    # zip 파일 경로 리턴
    return HttpResponse(DATA_DIR.replace("\\","/") + "/data/zip/" + userid + ".zip")

# zip 파일 다운로드 함수
def zipdownload(request):

    # zip 파일 경로를 통해 파일 리턴
    return FileResponse(open(request.GET["path"], "rb"))


def folderlist(request):
    # 세션에 존재하는 디렉토리 경로를 불러와 dirpath 변수에 저장    
    dirpath = request.session['dirpath']

    # 세션에 현재 디렉토리 정보(dir)가 세션에 존재하는지 확인
    if request.session.has_key('dir'):
        # 존재할 시 dirpath 정보 값을 기존 정보와 dir 세션 정보 통합
        dirpath = dirpath + "/" + request.session['dir']
    
    # GET 통신 데이터 folder를 변수 folder에 대입
    folder = request.GET['folder']

    # dirpath 시작 경로로 personal과 team을 구분
    if(dirpath.startswith("personal")):
        # Personal Storage 사용자 선택 경로 폴더명들 저장
        folder_list = PSInfo.objects.filter(file__startswith = dirpath + "/" + folder).exclude(filename__contains = ".").order_by('filename').values('filename')
    else:
        # Team Storage 사용자 선택 경로 폴더명들 저장
        folder_list = TSInfo.objects.filter(file__startswith = dirpath + "/" + folder).exclude(filename__contains = ".").order_by('filename').values('filename')
    
    # folder_data list 형식 변수 선언
    folder_data = []

    for temp in folder_list:
        folder_data.append(temp['filename'])

    data = { "folderlist" : folder_data }

    return JsonResponse(data)


def deleteuser(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    if TeamStorage.objects.filter(master_id = userid).exists() == True:
        return HttpResponse("fail")

    user = User.objects.get(pk = userid)
    
    PSInfo.objects.filter(file__startswith = "personal/" + userid).delete()

    # 상위 폴더 이동
    os.chdir("..")

    # data 디렉토리로 이동
    os.chdir("./data")

    # 디렉토리 내부까지 전부 삭제
    shutil.rmtree("./personal/" + userid)
    
    # 웹 서버 경로로 이동
    os.chdir(position)

    User.objects.filter(user_id = userid).delete()

    return HttpResponse("success")


def findid(request):

    name = request.GET['name']

    phone = request.GET['phone']

    if User.objects.filter(user_name = name, user_phone = phone).exists() == True:
        value = User.objects.get(user_name = name, user_phone = phone)

        findid = value.user_id

        b = ""

        for i in range(3,len(findid)):
            b += '*'

        result = findid[:3] + b

        return HttpResponse(result)
    
    return HttpResponse("fail")


def checkuser(request):

    user_id = request.GET['id']

    phone = request.GET['phone']

    if User.objects.filter(user_id = user_id, user_phone = phone).exists() == True:
        return HttpResponse("exist")

    return HttpResponse("fail")


def resetpw(request):

    user_id = request.GET['id']

    pw = request.GET['pw']

    User.objects.filter(user_id = user_id).update(user_pw = pw)

    return HttpResponse()

def changeemo(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    emo = request.GET['emo']

    User.objects.filter(user_id = userid).update(user_emo = emo)

    return HttpResponse("이모티콘 변경이 완료되었습니다.")