from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from main.models import User

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
    
    return render(request, 'Index.html')

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