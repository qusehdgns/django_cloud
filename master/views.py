from django.shortcuts import render

# Create your views here.
def ts_master(request):
    return render(request, "TS_Master.html")

def ts_notice_upload(request):
    return render(request, "TS_Notice_Upload.html")