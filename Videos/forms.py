from django import forms
from Videos.models import Video, Comment


class VideoUploadForm(forms.ModelForm):
    thumbnail = forms.ImageField(required=False)

    class Meta:
        model = Video
        fields = ['video', 'thumbnail', 'name', 'description', 'category']


