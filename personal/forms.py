from django import forms

from personal.models import PSInfo

class PSInfoForm(forms.ModelForm):
    class Meta:
        model = PSInfo
        fields = ['filename', 'file', 'descript']