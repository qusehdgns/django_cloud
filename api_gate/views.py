# 웹에 문자열 리턴
from django.http import HttpResponse
# 파일 정보 리턴
from django.http import FileResponse
# Post 통신 시 필요한 암호화를 우회
from django.views.decorators.csrf import csrf_exempt
# 데이터 저장 경로 확인(데이터 경로)
from cloud.settings import DATA_DIR

# 파일 관련 함수 사용
import os
# 디렉토리 관련 함수
import shutil

# 데이터 베이스 연동 기능
# main App의 models.py 내부 class 선언
from main.models import User
# personal App의 models.py 내부 class 선언
from personal.models import  PSInfo, setdir

# personal App에 forms.py 내부 PSInfoForm
from personal.forms import PSInfoForm

# 초기 디렉터리 저장(웹 서버 경로)
position = os.getcwd()

def api_login(request):
    userid = request.GET['userid']
    pw = request.GET['userpw']

    if User.objects.filter(user_id = userid, user_pw = pw).exists() == True:

        return HttpResponse("success")

    return HttpResponse("fail")

def api_idcheck(request):
    if User.objects.filter(user_id = request.GET["userid"]).exists() == True :
        return HttpResponse("fail")

    return HttpResponse("success")

def api_signin(request):
    data = request.GET;

    User.objects.create(user_id = data['userid'], user_pw = data['userpw'], user_name = data['username'], user_phone = data['userphone'])

    os.chdir("../data/personal")

    os.makedirs(data['userid'])

    os.chdir(position)
    
    return HttpResponse('success')

def api_storage(request):
    data = ""

    userid = request.GET['userid']

    dirpath = "personal/" + userid

    os.chdir("../data/" + dirpath)

    file_list = os.listdir("./")

    os.chdir(position)

    data += userid

    for temp in file_list:
        data += ">" + temp

    return HttpResponse(data)


def api_download(request):

    data = request.GET

    dirpath = "personal/" + data['userid']  + "/" + data['file']

    return FileResponse(open("../data/" + dirpath, "rb"))

@csrf_exempt
def api_upload(request):

    data = request.GET

    dirpath = "personal/" + data['userid']

    psinfo = PSInfo.objects

    filename = request.POST['filename']

    temp = filename.replace(" ", "_")

    setdir(dirpath)

    if psinfo.filter(file = dirpath + "/" + temp).exists() == True:

        psinfo.filter(file = dirpath + "/" + temp).delete()

        os.chdir("..")

        os.chdir("./data")

        os.remove("./" + dirpath + "/" + temp)

        os.chdir(position)

    form = PSInfoForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        return HttpResponse("success")
    else:
        print(form.errors)
    
    return HttpResponse("fail")

def api_delete(request):
    data = request.GET

    dirpath = "personal/" + data['userid']

    psinfo = PSInfo.objects

    filename = data['file']

    temp = filename.replace(" ", "_")

    psinfo.filter(file = dirpath + "/" + temp).delete()

    os.chdir("../data")

    os.remove("./" + dirpath + "/" + temp)

    os.chdir(position)

    return HttpResponse("success")