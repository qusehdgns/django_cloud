from django.contrib import admin
from master.models import TeamStorage

# 출력할 ResourceAdmin 클래스를 만든다
class TeamStorageAdmin(admin.ModelAdmin):
    list_display = ('storage_name', 'description', 'authority', 'master_id')

# 클래스를 어드민 사이트에 등록한다.
admin.site.register(TeamStorage, TeamStorageAdmin)