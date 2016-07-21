# -*- coding:utf-8 -*-
#author:hjd
from django import forms
class FileForm(forms.Form):
    UploadFile = forms.FileField(label='文件',required=False)