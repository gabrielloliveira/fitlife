from django.urls import path
from . import views

app_name = "practice"

urlpatterns = [
    path("", views.list_practice, name="list"),
    path("adicionar/", views.add_practice, name="create"),
    path("<uuid:uuid>/deletar/", views.delete_practice, name="delete"),
]
