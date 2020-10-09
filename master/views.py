from django.shortcuts import render

# main App의 models.py 내부 class 선언
from main.models import StorageList

# http://localhost:8000/master/
# TeamStorage Master 페이지 이동 함수
def ts_master(request):
    # 세션에서 userid 호출
    userid = request.session['userid']

    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # StorageList 내부에서 선택 teamstorage의 사용자 ID, 권한 호출
    # sql : select user_id, personal_auth from storagelist where team_storage = 변수ts_name;
    user_result = StorageList.objects.filter(team_storage = ts_name).values("user_id", "personal_auth")

    # list 선언 ( 배열 )
    user_data = []

    # select 결과값만 list로 변환
    for temp in user_result:
        user = { 'userid' : temp['user_id'], 'auth' : temp['personal_auth']}
        user_data.append(user)

    # TS_Master.html 반환 시 TeamStorage이름, 유저ID, TeamStorage 사용자 정보 반환
    return render(request, "TS_Master.html", { 'ts_name' : ts_name, 'userid' : userid, 'data' : user_data })

# http://localhost:8000/master/ts_notice_upload
# 공지사항 작성 페이지 호출
def ts_notice_upload(request):
    # 세션 team storage 이름 호출
    ts_name = request.session['ts_name']

    # TS_Master.html 반환 시 TeamStorage이름 반환
    return render(request, "TS_Notice_Upload.html", { 'ts_name' : ts_name })