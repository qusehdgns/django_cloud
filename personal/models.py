from django.db import models

# 파일 저장 경로 설정 변수
dir_path = str()

# 파일 저장 경로 설정 함수
def setdir(request):
    # 전역 변수 호출
    global dir_path

    # 요청값 전역 변수에 대입
    dir_path = request

# 데이터베이스 저장 호출 함수
def user_directory_path(instance, filename):
    # 전역 변수 호출
    global dir_path

    # 파일 저장 경로와 파일 이름 결합 후 리턴
    return dir_path + "/" + filename

# Personal Storage 데이터베이스
class PSInfo(models.Model):
    # 파일 명
    filename = models.CharField(max_length=100)

    # 파일 경로 및 파일
    file = models.FileField(upload_to=user_directory_path)
   
    # 주석 및 메모
    descript = models.TextField(blank = True, null = True)

    class Meta:
        # 데이터베이스 테이블 명 'PersonalStorageInfo'
        db_table = 'PersonalStorageInfo'

