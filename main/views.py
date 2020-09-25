from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'Login.html')

def index(request):
    return render(request, 'Index.html')

def profile(request):
    return render(request, 'Profile.html')

def sign_in(request):
    return render(request, 'Sign_in.html')

def find_id_reset_pw(request):
    return render(request, 'Find_ID_Reset_PW.html')