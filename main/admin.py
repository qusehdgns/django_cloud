from django.contrib import admin
from main.models import User
from main.models import StorageList
from master.models import TeamStorage

# 출력할 ResourceAdmin 클래스를 만든다
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_pw', 'user_name', 'user_phone')

class StorageListAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'team_storage', 'personal_auth')

class TeamStorageAdmin(admin.ModelAdmin):
    list_display = ('storage_name', 'description', 'authority', 'master_id')

# 클래스를 어드민 사이트에 등록한다.
admin.site.register(User, UserAdmin)
admin.site.register(StorageList, StorageListAdmin)
admin.site.register(TeamStorage, TeamStorageAdmin)