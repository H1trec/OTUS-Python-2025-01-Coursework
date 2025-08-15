""" Сервисный слой по пользователям """
from django.contrib.auth import get_user_model
from ..models import Registration, Waitlist

User = get_user_model()


def get_user_events(user_id):
    user = User.objects.get(pk=user_id)
    registrations = Registration.objects.filter(user=user).select_related('event')
    waitlists = Waitlist.objects.filter(user=user).select_related('event')

    return {
        'registrations': registrations,
        'waitlists': waitlists,
    }


def block_user(user_id):
    user = User.objects.get(pk=user_id)
    user.is_blocked = True
    user.save()
    return user


def unblock_user(user_id):
    user = User.objects.get(pk=user_id)
    user.is_blocked = False
    user.save()
    return user