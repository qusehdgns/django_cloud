from django.db import models

# 사용자 데이터베이스
class User(models.Model):
    # 사용자 ID (PK)
    user_id = models.CharField(max_length=50, primary_key=True)
    
    # 사용자 PW
    user_pw = models.CharField(max_length=50)

    # 사용자 이름
    user_name = models.CharField(max_length=50)

    # 사용자 전화번호
    user_phone = models.CharField(max_length=50)

    class Meta:
        # 데이터베이스 테이블 명 'users'
        db_table = 'users'

# 사용자 Team Storage 데이터베이스
class StorageList(models.Model):
    # 사용자 ID (FK)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # Team Storage 이름 (FK)
    team_storage = models.ForeignKey("master.TeamStorage", on_delete=models.CASCADE)

    # 사용자 권한
    personal_auth = models.IntegerField()

    class Meta:
        # 데이터베이스 테이블 명 'storagelists'ss
        db_table = 'storagelists'

