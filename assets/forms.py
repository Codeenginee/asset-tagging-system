from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )


class ImageUploadForm(forms.Form):

    images = forms.ImageField(

        widget=forms.ClearableFileInput(

            attrs={

                "multiple": True

            }

        )

    )


class BulkUploadForm(forms.Form):

    dataset_name = forms.CharField(
        max_length=255
    )

    images = forms.FileField(
        required=True
    )

