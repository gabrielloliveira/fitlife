from django.urls import path
from . import views

app_name = "practice"

urlpatterns = [
    path("", views.list_practice, name="list"),
]
