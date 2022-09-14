from django.urls import path
from . import views

app_name = "practice"

urlpatterns = [
    path("", views.list_practice, name="list"),
    path("adicionar/", views.add_practice, name="create"),
    path("<uuid:uuid>/deletar/", views.delete_practice, name="delete"),
    path("<uuid:uuid>/editar/", views.edit_practice, name="edit"),
    path("<uuid:uuid>/detalhes/", views.detail_practice, name="detail"),
    path("<uuid:uuid>/detalhes/cadastrar-exercicio/", views.add_exercise, name="create-exercise"),
    path("<uuid:uuid>/detalhes/<uuid:uuid_exercise>/deletar/", views.delete_exercise, name="delete-exercise"),
    path("<uuid:uuid>/detalhes/<uuid:uuid_exercise>/editar/", views.edit_exercise, name="edit-exercise"),
    path("frequencia/iniciar/", views.start_frequency, name="start-frequency"),
    path("frequencia/finalizar/", views.end_frequency, name="end-frequency"),
    path("exercicio/<uuid:uuid>/check/", views.check_exercise, name="check"),
]
