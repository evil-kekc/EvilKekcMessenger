from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
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
    user = request.user

    chat_list = Message.objects.filter(
        Q(sender=user) | Q(recipient=user)
    ).values('sender', 'recipient').distinct()

    chat_ids = {chat['sender'] if chat['sender'] != user.id else chat['recipient'] for chat in chat_list}

    chats = []
    for chat_id in chat_ids:
        other_user = User.objects.get(id=chat_id)
        last_message = Message.objects.filter(
            (Q(sender=user, recipient=other_user) | Q(sender=other_user, recipient=user))
        ).order_by('-timestamp').first()
        chat_info = {
            'user': other_user,
            'last_message': last_message,
        }
        chats.append(chat_info)

    context = {
        'chats': chats,
    }
    return render(request, 'account/home.html', context)


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
    :return: HTTP Response
    """
    user = get_object_or_404(User, username=username)

    context = {
        'user': user,
    }
    return render(request, 'account/user_detail.html', context)


@login_required
def chat_view(request, username: str):
    """Chat with user

    :param username: username
    :param request: request object
    :return: HTTP Response
    """
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            recipient = User.objects.get(username=username)
            Message.objects.create(content=message, sender=request.user, recipient=recipient)
            return redirect('chat', username=username)

    messages = Message.objects.filter(
        Q(sender__username=request.user, recipient__username=username) | Q(sender__username=username,
                                                                           recipient__username=request.user))
    context = {
        'messages': messages,
        'username': username,
    }
    return render(request, 'chat.html', context)
