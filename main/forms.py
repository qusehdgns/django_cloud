from django import forms

from main.models import PSInfo

class PSInfoForm(forms.ModelForm):
    class Meta:
        model = PSInfo
        fields = ('name', 'file', 'memo')