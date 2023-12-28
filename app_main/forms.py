from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import ModelForm, Select

from app_main.models import Profile


class FileUploadForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(['xlsx'])])



class ProfileForm(ModelForm):
    username = forms.CharField(required=True, label='Nazwa użytkownika')
    email = forms.EmailField(required=True, label='Adres email')
    
    class Meta:
        model = Profile
        fields = ['username', 'email', 'rank']
        labels = {
            'username': 'Nazwa użytkownika',
            'email': 'Adres email',
            'rank': 'Ranga',
        }
        widgets = {
            'rank': Select(attrs={'class': 'js-example-basic-single'}),
        }