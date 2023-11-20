from django import forms

from database.models import films

class UploadFilm(forms.Forms):
    title = forms.CharField(max_length=128)
    description = forms.CharField(max_length=500)
    genre = forms.CharField(max_length=100)
    data = forms.FileField()


    class Meta:
        model = films
        fields = ('title', 'description', 'genre', 'data')