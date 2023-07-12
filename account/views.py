from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Message


@login_required
def home(request):
    """Home page view

    :param request: request object
    :return: HTTP Response
    """
    messages = Message.objects.all()

    context = {
        'messages': messages,
        'selection': 'dashboard'
    }
    return render(
        request,
        'account/home.html',
        context
    )
