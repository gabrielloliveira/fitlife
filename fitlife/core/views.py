from django.contrib.auth.views import LoginView
from django.shortcuts import render


index = LoginView.as_view(template_name="core/login.html", redirect_authenticated_user=True)
