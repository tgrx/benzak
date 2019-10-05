from platform import system

from django.shortcuts import render


def get_alco():
    return ["Jim Beam", "Vodka", "Pivo"]


def index(request):
    return render(request, "index.html", {"alco": get_alco(), "title": "Main"})
