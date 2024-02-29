from django import forms
from .models import Video, Report


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'file']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['video', 'report', 'total']
