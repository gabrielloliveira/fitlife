from django.urls import path

from . import views


app_name = "core"

urlpatterns = [
    path("", views.login, name="login"),
    path("sair/", views.logout, name="logout"),
    path("home/", views.home, name="home"),
    path("equipe/", views.collaborators, name="collaborators"),
    path("equipe/adicionar/", views.add_collaborator, name="add-collaborator"),
]
