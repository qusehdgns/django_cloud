from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse

import json

from main.models import User, StorageList

# Create your views here.
def login(request):
    if request.method == "POST":
        data = request.POST;
        if User.objects.filter(user_id = data['userid'], user_pw = data['userpw']).exists() == True :
            request.session['userid'] = data['userid']
            return redirect('personal_storage')
        else:
            return HttpResponse()
    return render(request, 'Login.html')

def index(request):
    userid = request.session['userid']

    user_result = User.objects.get(pk = userid)

    user_data = { "userid" : user_result.user_id, "username" : user_result.user_name }

    ts_result = StorageList.objects.filter(user_id = userid).values("team_storage")

    ts_data = []

    for temp in ts_result:
        ts_data.append(temp['team_storage'])

    data = { "user" : user_data, "storage" : ts_data }
    
    return JsonResponse(data)

def profile(request):
    return render(request, 'Profile.html')

def sign_in(request):
    # Post 요청 시 실행
    if request.method == "POST":
        data = request.POST;
        User.objects.create(user_id = data['userid'], user_pw = data['userpw'], user_name = data['username'], user_phone = data['userphone'])
        return redirect('login')
        
    return render(request, 'Sign_in.html')

def find_id_reset_pw(request):
    return render(request, 'Find_ID_Reset_PW.html')

def logout(request):
    request.session.pop('userid')
    return redirect('login')

def movetots(request):

    storage_name = request.GET['name']

    request.session['ts_name'] = storage_name
    
    return redirect('team_storage')