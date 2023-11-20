from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

from database.models import films

class UploadFilm(forms.ModelForm):
    title = forms.CharField(primary_key=True, max_length=128, unique= True)
    path = forms.FileField(upload_to='cinema')
    rating = forms.DecimalField(max_digits=6, decimal_places= 2)

    class Meta:
        model = films
        fields = ('title', 'rating', 'path')
