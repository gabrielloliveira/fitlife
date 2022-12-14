import datetime
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from fitlife.core.decorators import admin_required
from fitlife.core.models import User
from fitlife.practice.forms import PracticeForm, ExerciseForm
from fitlife.practice.models import Practice, Exercise, Frequency, Checklist


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
@admin_required
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
@admin_required
def delete_practice(request, uuid):
    practice = get_object_or_404(Practice, uuid=uuid)
    practice.delete()
    messages.success(request, "Treino deletado com sucesso.")
    return HttpResponseRedirect(reverse("practice:list"))


@require_POST
@login_required
@admin_required
def edit_practice(request, uuid):
    practice = get_object_or_404(Practice, uuid=uuid)
    form = PracticeForm(request.POST, instance=practice, prefix=f"{practice.uuid}")
    if form.is_valid():
        form.save()
        messages.success(request, "Treino atualizado com sucesso.")
    else:
        print(form.errors)
        messages.error(request, "Erro ao atualizar o treino.", extra_tags="danger")
    return HttpResponseRedirect(reverse("practice:list"))


@login_required
@admin_required
def detail_practice(request, uuid):
    practice = get_object_or_404(Practice, uuid=uuid)
    context = {
        "practice": practice,
        "exercises": practice.exercise_set.order_by("day"),
        "form": ExerciseForm(),
    }
    return render(request, "practice/detail.html", context=context)


@require_POST
@login_required
@admin_required
def add_exercise(request, uuid):
    form = ExerciseForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Exerc??cio vinculado com sucesso.")
    else:
        print(form.errors)
        messages.error(request, "Erro ao vincular exerc??cio.", extra_tags="danger")
    return HttpResponseRedirect(reverse("practice:detail", kwargs={"uuid": uuid}))


@require_POST
@login_required
@admin_required
def delete_exercise(request, uuid, uuid_exercise):
    exercise = get_object_or_404(Exercise, practice__uuid=uuid, uuid=uuid_exercise)
    exercise.delete()
    messages.success(request, "Exerc??cio deletado com sucesso.")
    return HttpResponseRedirect(reverse("practice:detail", kwargs={"uuid": uuid}))


@require_POST
@login_required
@admin_required
def edit_exercise(request, uuid, uuid_exercise):
    exercise = get_object_or_404(Exercise, practice__uuid=uuid, uuid=uuid_exercise)
    form = ExerciseForm(request.POST, instance=exercise, prefix=f"{exercise.uuid}")
    if form.is_valid():
        form.save()
        messages.success(request, "Exerc??cio atualizado com sucesso.")
    else:
        print(form.errors)
        messages.error(request, "Erro ao atualizar exerc??cio.", extra_tags="danger")
    return HttpResponseRedirect(reverse("practice:detail", kwargs={"uuid": uuid}))


@require_POST
@login_required
def start_frequency(request):
    Frequency.objects.create(user=request.user, date_start=timezone.now())
    return HttpResponseRedirect(reverse("core:practice"))


@require_POST
@login_required
def end_frequency(request):
    Frequency.objects.filter(user=request.user, date_start__date=timezone.now().date()).update(date_end=timezone.now())
    return HttpResponseRedirect(reverse("core:practice"))


@login_required
@require_POST
def check_exercise(request, uuid):
    exercise = get_object_or_404(Exercise, uuid=uuid)
    Checklist.objects.create(
        date=date.today(),
        exercise=exercise,
        user=request.user,
    )
    return HttpResponseRedirect(reverse("core:practice"))
