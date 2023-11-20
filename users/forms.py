from typing import Any
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic.edit import ModelFormMixin
from database.models import user, articles

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Password does not math')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    surname = forms.CharField(max_length=200, help_text='Required')
    name = forms.CharField(max_length=200, help_text='Required')
    patronimic = forms.CharField(max_length=200, help_text='Required')

    class Meta:
        model = user
        fields = ('name', 'surname', 'patronimic', 'username', 'email', 'password1', 'password2')




class UpdateUserForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    email = forms.EmailField(max_length=200, required=False)
    surname = forms.CharField(max_length=200, required=False)
    name = forms.CharField(max_length=200, required=False)
    patronimic = forms.CharField(max_length=200, required=False)
    

    class Meta:
        model = user
        fields = ('username', 'email', 'surname', 'name', 'patronimic')


class UploadForm(forms.ModelForm):
    class Meta:
        model = articles
        fields = ['title', 'path']
    def is_valid(self, id) -> bool:
        # print(id)
        # print(self.__dict__['data']['id_author'])
        # self.__dict__['data']['id_author'] = id
        return super().is_valid()
    
    