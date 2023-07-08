from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from setup import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", lambda req: redirect('/equipment'), name="index"),
    path('', include("apps.user.urls")),
    path('', include("apps.equipment.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
