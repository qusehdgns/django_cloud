from django.shortcuts import render

from main.models import StorageList

# Create your views here.
def team_storage(request):

    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    return render(request, "Team_Storage.html", { 'name' : ts_name })

def team_storage_list(request):

    # 세션에서 userid 호출
    userid = request.session['userid']

    # sql : select team_storage from storagelist where user_id = 변수userid;
    ts_result = StorageList.objects.filter(user_id = userid).values("team_storage")

    # list 선언 ( 배열 )
    ts_data = []

    # select 결과값만 list로 변환
    for temp in ts_result:
        ts_data.append(temp['team_storage'])

    
    return render(request, "Team_Storage_List.html", { "data" : ts_data })

def team_storage_create(request):
    return render(request, "Team_Storage_Create.html")

def ts_file_upload(request):
    return render(request, "TS_File_Upload.html")