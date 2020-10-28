from django.db import models
# 시스템 시간값 라이브러리
import datetime

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

# Team Storage 파일 데이터베이스
class TSInfo(models.Model):
    # 파일 명
    filename = models.CharField(max_length=100)

    # 파일 경로 및 파일
    file = models.FileField(upload_to=user_directory_path)
   
    # 주석 및 메모
    descript = models.TextField(blank = True, null = True)

    # 접근 권한
    access_auth = models.IntegerField()

    class Meta:
        # 데이터베이스 테이블 명 'TeamStorageInfo'
        db_table = 'TeamStorageInfo'


# Team Notice 데이터베이스
class Notice(models.Model):
    # Team Storage 이름 (FK)
    team_storage = models.ForeignKey("master.TeamStorage", on_delete=models.CASCADE)

    # 게시물 작성자 (FK)
    author = models.ForeignKey("main.User", on_delete=models.CASCADE)

    # 게시물 제목
    title = models.CharField(max_length=250)

    # 게시물 내용
    value = models.TextField(blank = False, null = False)

    # 입력 시간
    input_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 데이터베이스 테이블 명 'TeamNotice'
        db_table = 'TeamNotice'
        # 복합 중복 방지 ( 중복 공지 제목 방지 )
        unique_together = (('team_storage', 'title'),)