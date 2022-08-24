from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from fitlife.core.models import User
from fitlife.practice.forms import PracticeForm
from fitlife.practice.models import Practice


@login_required
def list_practice(request):
    context = {
        "practices": Practice.objects.all(),
        "form": PracticeForm(),
        "students": User.objects.only_students(),
    }
    return render(request, "practice/list.html", context=context)


@require_POST
@login_required
def add_practice(request):
    form = PracticeForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Treino cadastrado com sucesso.")
    else:
        print(form.errors)
        messages.error(request, "Erro ao cadastrar treino.", extra_tags="danger")
    return HttpResponseRedirect(reverse("practice:list"))


@require_POST
@login_required
def delete_practice(request, uuid):
    practice = get_object_or_404(Practice, uuid=uuid)
    practice.delete()
    messages.success(request, "Treino deletado com sucesso.")
    return HttpResponseRedirect(reverse("practice:list"))


@require_POST
@login_required
def edit_practice(request, uuid):
    practice = get_object_or_404(Practice, uuid=uuid)
    form = PracticeForm(request.POST, instance=practice)
    if form.is_valid():
        form.save()
        messages.success(request, "Treino atualizado com sucesso.")
    else:
        print(form.errors)
        messages.error(request, "Erro ao atualizar o treino.", extra_tags="danger")
    return HttpResponseRedirect(reverse("practice:list"))
