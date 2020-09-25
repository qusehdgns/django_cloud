from django.shortcuts import render

# Create your views here.
def personal_storage(request):
    return render(request, 'Personal_Storage.html')

def ps_file_upload(request):
    return render(request, 'PS_File_Upload.html')