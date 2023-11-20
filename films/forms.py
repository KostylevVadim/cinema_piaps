
from django import forms

class Commentform(forms.Form):
    text = forms.CharField(widget= forms.TextInput(attrs= {
        'class':'form-control py-4', 'placeholder': 'Введите текст'
    }))
    id_prev = forms.IntegerField(required=False)

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

from database.models import films

# class UploadFilm(forms.ModelForm):
#     title = forms.CharField(max_length=128)
#     description = forms.CharField(max_length=500)
#     path = forms.FileField(upload_to='cinema')
#     rating = forms.DecimalField(max_digits=6, decimal_places= 2)

#     class Meta:
#         model = films
#         fields = ('title', 'rating', 'path')


class UploadForm(forms.ModelForm):
    class Meta:
        model = films
        fields = ['title', 'path']
    def is_valid(self, id) -> bool:
        # print(id)
        # print(self.__dict__['data']['id_author'])
        # self.__dict__['data']['id_author'] = id
        return super().is_valid()