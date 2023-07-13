from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Concat
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SearchForm, RegistrationForm
from .models import Message


def registration(request):
    """New User Registration

    :param request: request object
    :return: HTTP Response
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'registration/registration.html', context)


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


@login_required
def search(request):
    """Search people to connect

    :param request: request object
    :return: HTTP Response
    """
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        current_user = request.user.username
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = User.objects.annotate(
                similarity=TrigramSimilarity(Concat('username', 'first_name', 'last_name'), query),
            ).filter(similarity__gt=0.1).order_by('-similarity').exclude(username=current_user)

    context = {
        'form': form,
        'query': query,
        'results': results,
        'selection': 'search'
    }

    return render(request,
                  'account/peoples.html',
                  context)


@login_required
def user_page_view(request, username: str):
    """User detail page

    :param username: username
    :param request: request object
    :return:
    """
    user = get_object_or_404(User, username=username)

    context = {
        'user': user,
    }
    return render(request, 'account/user_detail.html', context)
