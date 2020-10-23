from django.db import models

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

