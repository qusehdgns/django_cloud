from django.contrib import admin
from personal.models import PSInfo

# 출력할 ResourceAdmin 클래스를 만든다
class PersonalStorageAdmin(admin.ModelAdmin):
    list_display = ('filename', 'file', 'descript')

# 클래스를 어드민 사이트에 등록한다.
admin.site.register(PSInfo, PersonalStorageAdmin)