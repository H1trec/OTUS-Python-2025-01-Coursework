"""Представления для пользователей"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from ..forms import UserRegistrationForm
from ..models import User
from ..services.user_service import get_user_events


def register_user(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'events/register_user.html', {'form': form})


@login_required
def user_profile(request):
    """Профиль пользователя"""
    user_events = get_user_events(request.user.id)
    return render(request, 'events/user_profile.html', {
        'registrations': user_events['registrations'],
        'waitlists': user_events['waitlists'],
    })