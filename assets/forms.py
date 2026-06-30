from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ImageUploadForm(forms.Form):

    images = forms.FileField(
        required=True
    )


class BulkUploadForm(forms.Form):

    dataset_name = forms.CharField(
        max_length=255
    )

    images = forms.FileField(
        required=True
    )

