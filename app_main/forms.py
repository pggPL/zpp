from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import FileExtensionValidator
from django.forms import ModelForm, Select

from app_main.models import Profile, Submission


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
    
    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        if user.rank == "Senior":
            user.is_staff = True
        else:
            user.is_staff = False
        if commit:
            user.save()
        return user


class LinkForm1(ModelForm):
    class Meta:
        model = Submission
        fields = ['category']
        labels = {
            'category': 'Kategoria',
        }
        widgets = {
            'category': Select(attrs={'class': 'js-example-basic-single'}),
        }


class LinkForm2(ModelForm):
    class Meta:
        model = Submission
        fields = ['link', 'category', 'platform']
        labels = {
            'link': 'Link',
            'category': 'Kategoria',
            'platform': 'Platforma',
        }

class ChangePasswordForm(PasswordChangeForm):
    # change labels
    old_password = forms.CharField(label='Stare hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Nowe hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Powtórz nowe hasło', widget=forms.PasswordInput(attrs={'class': 'form-control'}))