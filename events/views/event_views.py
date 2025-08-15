"""Представления для событий"""
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Event, Registration, Waitlist
from ..services.event_service import (
    register_for_event,
    cancel_registration
)
from ..utils.exceptions import NoAvailableSeats, UserBlocked as UserBlockedException

def event_list(request):
    """Список всех событий"""
    events = Event.objects.all().order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    """Детальная информация о событии"""
    event = get_object_or_404(
        Event.objects.prefetch_related(
            'event_registrations__user',
            'event_waitlists__user'
        ),
        pk=event_id
    )
    user = request.user

    # Получаем списки пользователей с дополнительной информацией

    registrations = event.event_registrations.select_related('user').order_by('seat_number')
    waitlist = event.event_waitlists.select_related('user').order_by('position')

    context = {
        'event': event,
        'registrations': registrations,
        'waitlist': waitlist,
        'is_registered': False,
        'is_waitlisted': False,
        'available_seats': event.max_seats - event.registered_count,
        'available_waitlist': event.max_waitlist - event.waitlist_count,
    }

    if user.is_authenticated:
        context.update({
            'is_registered': Registration.objects.filter(event=event, user=user).exists(),
            'is_waitlisted': Waitlist.objects.filter(event=event, user=user).exists(),
        })

    return render(request, 'events/event_detail.html', context)

@login_required
def register_for_event_view(request, event_id):
    """Обработка регистрации на событие"""
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        try:
            result = register_for_event(event_id, request.user.id)

            if result == "registered":
                messages.success(request, "Вы успешно зарегистрированы на событие")
            elif result == "waitlisted":
                waitlist_item = Waitlist.objects.get(event=event, user=request.user)
                return render(request, 'events/waitlisted.html', {
                    'event': event,
                    'position': waitlist_item.position
                })
            elif result == "already_registered":
                return render(request, 'events/already_registered.html', {
                    'event': event,
                    'registration': Registration.objects.get(event=event, user=request.user)
                })
            elif result == "already_in_waitlist":
                return render(request, 'events/already_waitlisted.html', {
                    'event': event,
                    'waitlist': Waitlist.objects.get(event=event, user=request.user)
                })

        except NoAvailableSeats:
            messages.error(request, "Извините, все места и позиции в листе ожидания заняты")
        except UserBlockedException:
            messages.error(request, "Ваш аккаунт заблокирован для регистрации на события")
        except Exception as e:
            messages.error(request, f"Произошла ошибка: {str(e)}")

    return redirect('event_detail', event_id=event.id)

@login_required
def cancel_registration_view(request, event_id):
    """Обработка отмены регистрации"""
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        try:
            result = cancel_registration(event_id, request.user.id)

            if result == "registration_canceled":
                messages.success(request, "Регистрация успешно отменена")
            elif result == "waitlist_canceled":
                messages.info(request, "Вы удалены из листа ожидания")
            else:
                messages.warning(request, "Вы не были зарегистрированы на это событие")

        except Exception as e:
            messages.error(request, f"Ошибка при отмене регистрации: {str(e)}")

    return redirect('event_detail', event_id=event.id)