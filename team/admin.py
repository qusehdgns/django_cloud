from django.contrib import admin
from team.models import TSInfo

# 출력할 ResourceAdmin 클래스를 만든다
class TeamStorageAdmin(admin.ModelAdmin):
    list_display = ('filename', 'file', 'descript', 'access_auth')

# 클래스를 어드민 사이트에 등록한다.
admin.site.register(TSInfo, TeamStorageAdmin)
