from django import forms
from Videos.models import Video


class VideoUploadForm(forms.ModelForm):
    thumbnail = forms.ImageField(required=False)

    class Meta:
        model = Video
        fields = ["video", "thumbnail", "name", "description", "category"]


class SearchForm(forms.Form):
    name = forms.CharField(label="Search by name", max_length=100)

    class Meta:
        model = Video
        fields = [
            "name",
        ]


class EditVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["video", "thumbnail", "name", "description", "category"]
