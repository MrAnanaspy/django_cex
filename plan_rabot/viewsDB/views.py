from django.contrib.postgres import serializers
from django.shortcuts import render
from itertools import chain
from django.http import JsonResponse
from .models import Appeal


def get_data(request):
    data = list(Appeal.objects.all())  # Получение всех объектов
    return render(request, "index.html", context={'data':data})

