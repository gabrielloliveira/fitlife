from django import forms

from fitlife.core.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(label="Senha", required=False)

    class Meta:
        model = User
        fields = ("name", "email", "password", "type")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["type"].required = True

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if self.data["password"]:
            user.set_password(self.data["password"])
        user.save()
        user.refresh_from_db()
        return user
