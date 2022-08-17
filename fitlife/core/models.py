import datetime
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from fitlife.core.managers import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("atualizado em"), auto_now_add=True)
    uuid = models.UUIDField(_("UUID"), editable=False, unique=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    TYPE_STUDENT = "student"
    TYPE_OWNER = "owner"
    TYPE_TRAINER = "trainer"
    TYPE_CHOICES = (
        (TYPE_TRAINER, _("Treinador")),
        (TYPE_STUDENT, _("Aluno")),
        (TYPE_OWNER, _("Gestor")),
    )

    email = models.EmailField(_("endereço de email"), unique=True)
    name = models.CharField(_("nome"), max_length=255)
    is_active = models.BooleanField(_("usuário está ativo?"), default=True)
    is_staff = models.BooleanField(_("é um membro da equipe?"), default=False)
    type = models.CharField(_("tipo de usuário"), max_length=20, choices=TYPE_CHOICES)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.name

    @property
    def last_entry(self):
        if self.type != self.TYPE_STUDENT:
            return None
        return datetime.date.today()
