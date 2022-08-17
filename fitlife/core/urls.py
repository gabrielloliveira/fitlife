from django.urls import path

from . import views


app_name = "core"

urlpatterns = [
    path("", views.login, name="login"),
    path("sair/", views.logout, name="logout"),
    path("home/", views.home, name="home"),
    path("equipe/", views.collaborators, name="collaborators"),
    path("equipe/adicionar/", views.add_collaborator, name="add-collaborator"),
    path("equipe/<uuid:uuid>/deletar/", views.delete_collaborator, name="delete-collaborator"),
    path("equipe/<uuid:uuid>/editar/", views.edit_collaborator, name="edit-collaborator"),
    path("alunos/", views.students, name="students"),
    path("alunos/adicionar/", views.add_student, name="add-student"),
    path("alunos/<uuid:uuid>/editar/", views.edit_student, name="edit-student"),
]
