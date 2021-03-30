from django import forms
from .models import BBSType,BBS
from .models import *
from django.forms import ModelForm

class BBSForm(ModelForm):
    class Meta:
        model = BBS#对应的Model中的类
        fields = ['title', 'bbs_type','content'] # 显示所有字段