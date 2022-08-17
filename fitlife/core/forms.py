from django import forms

from fitlife.core.models import User
from django.utils.translation import gettext_lazy as _


ADMIN_CHOICES = (
    (User.TYPE_TRAINER, _("Treinador")),
    (User.TYPE_OWNER, _("Gestor")),
)


class UserForm(forms.ModelForm):
    password = forms.CharField(label="Senha", required=False)
    type = forms.TypedChoiceField(choices=ADMIN_CHOICES)

    class Meta:
        model = User
        fields = ("name", "email", "password", "type")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["type"].required = True

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        user.save()
        user.refresh_from_db()
        return user


class StudentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "email", "password")

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields["password"].required = False

    def save(self, commit=True):
        user = super(StudentForm, self).save(commit=commit)
        user.type = User.TYPE_STUDENT
        user.save()
