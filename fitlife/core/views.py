from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from fitlife.core.forms import UserForm, StudentForm
from fitlife.core.models import User

login = LoginView.as_view(template_name="core/login.html", redirect_authenticated_user=True)
logout = LogoutView.as_view()


@login_required
def home(request):
    return render(request, "core/home.html")


@login_required
def collaborators(request):
    context = {
        "form": UserForm(initial={"type": "owner"}),
        "users": User.objects.exclude_students(),
    }
    return render(request, "core/collaborators.html", context=context)


@require_POST
@login_required
def add_collaborator(request):
    form = UserForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Funcionário cadastrado com sucesso.")
    else:
        print(form.errors)
        messages.error(request, "Erro ao cadastrar funcionário.", extra_tags="danger")
    return HttpResponseRedirect(reverse("core:collaborators"))


@require_POST
@login_required
def edit_collaborator(request, uuid):
    instance = get_object_or_404(User, uuid=uuid)

    instance.name = request.POST["name"]
    instance.email = request.POST["email"]
    instance.type = request.POST["type"]

    if request.POST["password"]:
        instance.set_password(request.POST["password"])

    instance.save()

    messages.success(request, "Funcionário editado com sucesso.")
    return HttpResponseRedirect(reverse("core:collaborators"))


@require_POST
@login_required
def delete_collaborator(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    user.delete()
    messages.success(request, "Funcionário deletado com sucesso.")
    return HttpResponseRedirect(reverse("core:collaborators"))


@login_required
def students(request):
    context = {
        "form": StudentForm(),
        "users": User.objects.only_students(),
    }
    return render(request, "core/students.html", context=context)


@require_POST
@login_required
def add_student(request):
    form = StudentForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Aluno cadastrado com sucesso.")
    else:
        print(form.errors)
        messages.error(request, "Erro ao cadastrar aluno.", extra_tags="danger")
    return HttpResponseRedirect(reverse("core:students"))


@require_POST
@login_required
def edit_student(request, uuid):
    instance = get_object_or_404(User, uuid=uuid)

    instance.name = request.POST["name"]
    instance.email = request.POST["email"]

    if request.POST["password"]:
        instance.set_password(request.POST["password"])

    instance.save()

    messages.success(request, "Aluno editado com sucesso.")
    return HttpResponseRedirect(reverse("core:students"))


@require_POST
@login_required
def delete_student(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    user.delete()
    messages.success(request, "Aluno deletado com sucesso.")
    return HttpResponseRedirect(reverse("core:students"))


class StudentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.only_students()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
