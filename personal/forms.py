from django import forms

# Personal App 내에 models.py 안 PSInfo 호출
from personal.models import PSInfo

# 데이터를 PSInfo 형식으로 저장가능한 클래스
class PSInfoForm(forms.ModelForm):
    class Meta:
        model = PSInfo
        fields = ['filename', 'file', 'descript']