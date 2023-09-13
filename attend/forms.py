# > 웹 상에서 데이터 입력받을 수 있는 폼 생성
from django import forms
from .models import Workers

class WorkersForm(forms.ModelForm):
    class Meta:
        model = Workers
        fields = ['w_id', 'wname', 'manager_id', 'contact', 'email']

        