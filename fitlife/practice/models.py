import calendar
import datetime

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField

from fitlife.core.models import BaseModel


class Practice(BaseModel):
    name = models.CharField(_("nome"), max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = _("Treino")
        verbose_name_plural = _("Treinos")

    def __str__(self):
        return self.name

    @property
    def get_form(self):
        from .forms import PracticeForm

        return PracticeForm(instance=self, prefix=f"{self.uuid}")

    @cached_property
    def students_id(self):
        return self.users.all().values_list("id", flat=True)

    @property
    def exercise_today(self):
        today = datetime.date.today().weekday()
        return self.exercise_set.filter(day=today).order_by("pk")

    def next_exercise(self, user):
        today = datetime.date.today()
        already_finished = user.checklist_set.filter(date__date=today).values_list("exercise_id")
        return self.exercise_set.filter(day=today.weekday()).exclude(id__in=already_finished).order_by("pk").first()


class Exercise(BaseModel):
    SUNDAY = calendar.SUNDAY
    MONDAY = calendar.MONDAY
    TUESDAY = calendar.TUESDAY
    WEDNESDAY = calendar.WEDNESDAY
    THURSDAY = calendar.THURSDAY
    FRIDAY = calendar.FRIDAY
    SATURDAY = calendar.SATURDAY

    DAYS_CHOICE = (
        (SUNDAY, _("Domingo")),
        (MONDAY, _("Segunda")),
        (TUESDAY, _("Terça")),
        (WEDNESDAY, _("Quarta")),
        (THURSDAY, _("Quinta")),
        (FRIDAY, _("Sexta")),
        (SATURDAY, _("Sábado")),
    )

    practice = models.ForeignKey("practice.Practice", verbose_name=_("Treino"), on_delete=models.CASCADE)
    day = models.IntegerField(_("dia da semana"), choices=DAYS_CHOICE)
    content = QuillField(verbose_name=_("conteúdo"))

    class Meta:
        verbose_name = _("Exercício")
        verbose_name_plural = _("Exercícios")

    def __str__(self):
        return f"{self.practice} | {self.day}"

    @property
    def get_form(self):
        from .forms import ExerciseForm

        return ExerciseForm(instance=self, prefix=f"{self.uuid}")


class Frequency(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("usuário"), on_delete=models.CASCADE)
    date_start = models.DateTimeField(_("entrada"))
    date_end = models.DateTimeField(_("saída"), blank=True, null=True)

    class Meta:
        verbose_name = _("Frequência")
        verbose_name_plural = _("Frequências")

    def __str__(self):
        return f"{self.user} | {self.date_start}"


class Checklist(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("usuário"), on_delete=models.CASCADE)
    exercise = models.ForeignKey("practice.Exercise", on_delete=models.CASCADE, verbose_name=_("exercício"))
    date = models.DateTimeField(_("dia"))

    class Meta:
        verbose_name = _("Checklist")
        verbose_name_plural = _("Checklists")

    def __str__(self):
        return f"{self.user} | {self.exercise} | {self.date}"
