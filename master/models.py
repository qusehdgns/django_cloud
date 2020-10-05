from django.db import models

# Create your models here.
class TeamStorage(models.Model):
    storage_name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=250)
    authority = models.IntegerField(default = 0)
    master_id = models.ForeignKey("main.User", on_delete=models.CASCADE)

    class Meta:
        db_table = 'teamstorages'