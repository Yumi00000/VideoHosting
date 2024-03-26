from django import forms
from Videos.models import Video


class VideoUploadForm(forms.ModelForm):
    thumbnail = forms.ImageField(required=False)

    class Meta:
        model = Video
        fields = ['video', 'thumbnail', 'name', 'description', 'category']


class VideoEditForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video', 'thumbnail', 'name', 'description', 'category']
