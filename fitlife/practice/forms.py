from dal import autocomplete
from django import forms
from django_quill.forms import QuillFormField

from fitlife.practice.models import Practice, Exercise


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


class ExerciseForm(forms.ModelForm):
    content = QuillFormField(label="Conteúdo")

    class Meta:
        model = Exercise
        fields = ("practice", "day", "content")
