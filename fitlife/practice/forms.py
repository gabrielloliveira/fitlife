from dal import autocomplete
from django import forms

from fitlife.practice.models import Practice


class PracticeForm(forms.ModelForm):
    class Meta:
        model = Practice
        fields = "__all__"
        widgets = {
            "users": autocomplete.ModelSelect2Multiple(
                url="core:student-autocomplete",
                attrs={
                    "data-placeholder": "Digite o nome do aluno ...",
                    "data-minimum-input-length": 2,
                },
            ),
        }
