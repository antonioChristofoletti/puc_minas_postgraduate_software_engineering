from apps.user.views import login
from apps.user.views import signout
from django.urls import path

urlpatterns = [
    path("login", login, name="login"),
    path("signout", signout, name="signout")
]
