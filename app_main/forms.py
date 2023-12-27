from django import forms
from django.core.validators import FileExtensionValidator


class FileUploadForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(['xlsx'])])
