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
    path("<uuid:uuid>/detalhes/<uuid:uuid_exercise>/", views.delete_exercise, name="delete-exercise"),
]
