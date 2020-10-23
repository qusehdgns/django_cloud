from django.db import models

dir_path = str()

def setdir(request):
    global dir_path
    dir_path = request

def user_directory_path(instance, filename):
    global dir_path
    return dir_path + "/" + filename

class PSInfo(models.Model):
    filename = models.CharField(max_length=100)
    file = models.FileField(upload_to=user_directory_path)
    descript = models.TextField(blank = True, null = True)

    class Meta:
        db_table = 'PersonalStorageInfo'

