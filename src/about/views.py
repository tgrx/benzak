from django.shortcuts import render

from about.models import Technology


def about(request):
    return render(
        request, "about/index.html", context={"technologies": Technology.objects.all()}
    )
