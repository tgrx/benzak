from django.core.signing import Signer
from django.shortcuts import render


def get_alco():
    signer = Signer()
    return tuple((v, signer.sign(v)) for v in ["Jim Beam", "Vodka", "Pivo"])


def index(request):
    return render(request, "index.html", {"alco": get_alco(), "title": "Main"})
