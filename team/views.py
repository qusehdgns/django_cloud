from django.shortcuts import render

# Create your views here.
def team_storage(request):
    return render(request, "Team_Storage.html")

def team_storage_list(request):
    return render(request, "Team_Storage_List.html")

def team_storage_create(request):
    return render(request, "Team_Storage_Create.html")

def ts_file_upload(request):
    return render(request, "TS_File_Upload.html")