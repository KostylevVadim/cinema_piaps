
from django import forms

class Commentform(forms.Form):
    text = forms.CharField(widget= forms.TextInput(attrs= {
        'class':'form-control py-4', 'placeholder': 'Введите текст'
    }))
    id_prev = forms.IntegerField(required=False)