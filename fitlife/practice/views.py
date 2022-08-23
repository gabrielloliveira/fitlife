from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from fitlife.practice.models import Practice


@login_required
def list_practice(request):
    context = {
        "practices": Practice.objects.all(),
    }
    return render(request, "practice/list.html", context=context)
