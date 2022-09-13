from datetime import datetime, date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from fitlife.core.models import User
from fitlife.practice.forms import PracticeForm, ExerciseForm
from fitlife.practice.models import Practice, Exercise, Frequency


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
    form = PracticeForm(request.POST, instance=practice, prefix=f"{practice.uuid}")
    if form.is_valid():
        form.save()
        messages.success(request, "Treino atualizado com sucesso.")
    else:
        print(form.errors)
        messages.error(request, "Erro ao atualizar o treino.", extra_tags="danger")
    return HttpResponseRedirect(reverse("practice:list"))


@login_required
def detail_practice(request, uuid):
    practice = get_object_or_404(Practice, uuid=uuid)
    context = {
        "practice": practice,
        "exercises": practice.exercise_set.order_by("-day"),
        "form": ExerciseForm(),
    }
    return render(request, "practice/detail.html", context=context)


@require_POST
@login_required
def add_exercise(request, uuid):
    form = ExerciseForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Exercício vinculado com sucesso.")
    else:
        print(form.errors)
        messages.error(request, "Erro ao vincular exercício.", extra_tags="danger")
    return HttpResponseRedirect(reverse("practice:detail", kwargs={"uuid": uuid}))


@require_POST
@login_required
def delete_exercise(request, uuid, uuid_exercise):
    exercise = get_object_or_404(Exercise, practice__uuid=uuid, uuid=uuid_exercise)
    exercise.delete()
    messages.success(request, "Exercício deletado com sucesso.")
    return HttpResponseRedirect(reverse("practice:detail", kwargs={"uuid": uuid}))


@require_POST
@login_required
def edit_exercise(request, uuid, uuid_exercise):
    exercise = get_object_or_404(Exercise, practice__uuid=uuid, uuid=uuid_exercise)
    form = ExerciseForm(request.POST, instance=exercise, prefix=f"{exercise.uuid}")
    if form.is_valid():
        form.save()
        messages.success(request, "Exercício atualizado com sucesso.")
    else:
        print(form.errors)
        messages.error(request, "Erro ao atualizar exercício.", extra_tags="danger")
    return HttpResponseRedirect(reverse("practice:detail", kwargs={"uuid": uuid}))


@require_POST
@login_required
def start_frequency(request, uuid):
    user = request.user
    queryset = Frequency.objects.filter(user=user, date_start__gte=date.today())
    if queryset.exist():
        return HttpResponseNotFound("Frequencia já registrada")

    Frequency.objects.create(user=user, date_start=datetime.now())
    return HttpResponse("ok")


@login_required
def frequency_is_active(request, uuid):
    user = request.user
    queryset = Frequency.objects.filter(user=user, date_start__gte=date.today())
    if not queryset.exist():
        return HttpResponseNotFound("Frequencia não existe")

    return HttpResponse("ok")


@require_POST
@login_required
def end_frequency(request, uuid):
    user = request.user
    frequency = get_object_or_404(Frequency, user=user, date_start__gte=date.today())
    frequency.date_end = datetime.now()
    frequency.save()
    return HttpResponse("ok")


@login_required
def count_frequency(request, uuid):
    user = request.user
    frequency_count = Frequency.objects.filter(user=user, date_start__gte=date.today(), date_end__isnull=True).count()
    return HttpResponse(str(frequency_count))
