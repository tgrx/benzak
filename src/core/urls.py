from django.contrib import admin
from django.http import HttpRequest
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def xxx(request: HttpRequest):
    from django.http import HttpResponse
    import json
    return HttpResponse(json.dumps({"method": request.method}), content_type="application/json")


urlpatterns = [
    path("", include("home.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
    path("dynamics/", include("dynamics.urls")),
    path("graphics/", include("graphics.urls")),
    path("xxx/", xxx),
]
