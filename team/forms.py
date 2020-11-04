from django import forms

# Team App 내에 models.py 안 PSInfo 호출
from team.models import TSInfo

# 데이터를 PSInfo 형식으로 저장가능한 클래스
class TSInfoForm(forms.ModelForm):
    class Meta:
        model = TSInfo
        fields = ['filename', 'file', 'descript', 'access_auth']