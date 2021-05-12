from django import forms
from .models import BarterType,Barter
from .models import *
from django.forms import ModelForm

class BarterForm(ModelForm):
    class Meta:
        model = Barter#对应的Model中的类
        fields = ['name', 'barter_type', 'content', 'image', 'want_barter','where'] # 显示所有字段