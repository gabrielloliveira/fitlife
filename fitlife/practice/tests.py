from fitlife.core.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from fitlife.practice.models import Practice


class Admin(TestCase):
    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(
            email="teste1@teste.com",
            name="test",
            type=User.TYPE_TRAINER,
            is_staff=True,
            password="test",
        )
        self.client = Client()

    def test_get_alunos(self):
        self.client.login(username="teste1@teste.com", password="test")
        response = self.client.get("/alunos/")
        self.assertEqual(response.status_code, 200)

    def test_alunos_add(self):
        self.client.login(username="teste1@teste.com", password="test")
        response = self.client.post("/alunos/adicionar/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_equipes(self):
        self.client.login(username="teste1@teste.com", password="test")
        response = self.client.get("/equipe/")
        self.assertEqual(response.status_code, 200)

    def test_equipe_add(self):
        self.client.login(username="teste1@teste.com", password="test")
        response = self.client.post("/equipe/adicionar/", follow=True)
        self.assertEqual(response.status_code, 200)
