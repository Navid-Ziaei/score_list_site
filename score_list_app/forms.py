from django.forms import ModelForm
from .models import ToDo, UploadFile
from django import forms
from .validators import validate_file_extension


class TodoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'memo', 'important']


class UploadForm(ModelForm):
    class Meta:
        model = UploadFile
        fields = ['upload']


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_extension])
