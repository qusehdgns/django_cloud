from django.contrib import admin
from main.models import User, StorageList

# 출력할 ResourceAdmin 클래스를 만든다
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_pw', 'user_name', 'user_phone', 'user_emo')

class StorageListAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'team_storage', 'personal_auth')

# 클래스를 어드민 사이트에 등록한다.
admin.site.register(User, UserAdmin)
admin.site.register(StorageList, StorageListAdmin)