from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def redirect_not_auth_user(request: WSGIRequest) -> HttpResponseRedirect:
    if not request.user.is_authenticated:
        messages.error(request, 'User is not authenticated.')
        return redirect('login')
