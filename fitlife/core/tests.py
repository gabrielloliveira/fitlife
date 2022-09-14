from fitlife.core.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from fitlife.practice.models import Practice


# Create your tests here.


class Alunos(TestCase):
    @classmethod
    def setUp(self):
        self.user = User.objects.create_user(
            email="teste@teste.com",
            name="test",
            type="student",
            password="test",
        )
        self.client = Client()

    def test_meu_treino(self):
        practice = Practice.objects.create(
            name="Treino B",
        )
        practice.users.add(self.user)
        practice.save()
        self.client.login(username="teste@teste.com", password="test")
        response = self.client.get("/meu-treino/")
        self.assertEqual(response.status_code, 200)

    def test_frequency_inicar(self):
        self.client.login(username="teste@teste.com", password="test")
        practice = Practice.objects.create(
            name="Treino B",
        )
        practice.users.add(self.user)
        practice.save()
        response = self.client.post("/treinos/frequencia/iniciar/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_frequency_finalizar(self):
        self.client.login(username="teste@teste.com", password="test")
        practice = Practice.objects.create(
            name="Treino B",
        )
        practice.users.add(self.user)
        practice.save()
        response = self.client.post("/treinos/frequencia/finalizar/", follow=True)
        self.assertEqual(response.status_code, 200)

    # def test_alunos(self):
    #     self.client.login(username="teste@teste.com", password="test")
    #     response = self.client.get("/alunos/")
    #     self.assertEqual(response.status_code, 200)
