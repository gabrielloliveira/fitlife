from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("fitlife.core.urls", namespace="core")),
    path("treinos/", include("fitlife.practice.urls", namespace="practice")),
]
