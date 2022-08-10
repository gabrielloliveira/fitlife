from django import forms

from fitlife.core.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "email", "password", "type")
