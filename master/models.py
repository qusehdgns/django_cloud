from django.db import models

# Team Storage 데이터베이스
class TeamStorage(models.Model):
    # Storage 이름 (PK)
    storage_name = models.CharField(max_length=50, primary_key=True)
    
    # Storage 설명
    description = models.CharField(max_length=250)
    
    # Storage 마스터 제외 하위 계급
    authority = models.IntegerField(default = 1)
    
    # Master id
    master_id = models.ForeignKey("main.User", on_delete=models.CASCADE)

    class Meta:
        # 데이터베이스 테이블 명 'teamstorages'
        db_table = 'teamstorages'