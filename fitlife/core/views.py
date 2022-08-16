from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from fitlife.core.forms import UserForm
from fitlife.core.models import User

login = LoginView.as_view(template_name="core/login.html", redirect_authenticated_user=True)
logout = LogoutView.as_view()


@login_required
def home(request):
    return render(request, "core/home.html")


@login_required
def collaborators(request):
    context = {
        "form": UserForm(),
        "users": User.objects.filter(type__in=["owner", "trainer"])}
    return render(request, "core/collaborators.html", context=context)


@require_POST
@login_required
def add_collaborator(request):
    form = UserForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Funcionário cadastrado com sucesso.")
    else:
        messages.error(request, "Erro ao cadastrar funcionário.", extra_tags="danger")
    return HttpResponseRedirect(reverse("core:collaborators"))
