from django.db import models

dir_path = str()

def setdir(request):
    global dir_path
    dir_path = request

def user_directory_path(instance, filename):
    global dir_path
    return dir_path + "/" + filename

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    user_pw = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'

class StorageList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    team_storage = models.ForeignKey("master.TeamStorage", on_delete=models.CASCADE)
    personal_auth = models.IntegerField()

    class Meta:
        db_table = 'storagelists'

class PSInfo(models.Model):
    filename = models.CharField(max_length=100)
    file = models.FileField(upload_to=user_directory_path)
    descript = models.TextField(null = True)

    class Meta:
        db_table = 'PersonalStorageInfo'

