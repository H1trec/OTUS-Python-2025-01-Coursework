""" Реализация логики регистрации на события """
from django.conf import settings
from django.db import transaction
from ..utils.exceptions import NoAvailableSeats, UserBlocked
from ..models import Event, Registration, Waitlist, User
from ..utils.db import get_redis_connection

r = get_redis_connection()


def register_for_event(event_id: int, user_id: int) -> str:
    """
    Регистрирует пользователя на событие или в лист ожидания.
    Возвращает статус: 'registered', 'waitlisted', 'already_registered', 'already_in_waitlist'
    """
    lock = r.lock(f'event_register_{event_id}', timeout=settings.REDIS_LOCK_TIMEOUT)

    try:
        with lock, transaction.atomic():
            event = Event.objects.select_for_update().get(pk=event_id)
            user = User.objects.get(pk=user_id)

            # Проверка блокировки пользователя
            if user.is_blocked:
                raise UserBlocked()

            # Проверка существующих регистраций
            if Registration.objects.filter(event=event, user=user).exists():
                return "already_registered"
            if Waitlist.objects.filter(event=event, user=user).exists():
                return "already_in_waitlist"

            # Попытка основной регистрации
            if event.registered_count < event.max_seats:
                Registration.objects.create(
                    event=event,
                    user=user,
                    seat_number=Event.get_next_seat_number(event)
                )
                return "registered"

            # Попытка записи в лист ожидания
            if event.waitlist_count < event.max_waitlist:
                Waitlist.objects.create(
                    event=event,
                    user=user,
                    position=Event.get_next_waitlist_position(event)
                )
                return "waitlisted"

            raise NoAvailableSeats("Свободных мест нет.")

    except Exception as e:
        raise e


def cancel_registration(event_id: int, user_id: int) -> str:
    """
    Отменяет регистрацию пользователя.
    Возвращает статус: 'registration_canceled', 'waitlist_canceled', 'not_registered'
    """
    lock = r.lock(f'event_cancel_{event_id}', timeout=settings.REDIS_LOCK_TIMEOUT)

    try:
        with lock, transaction.atomic():
            event = Event.objects.select_for_update().get(pk=event_id)
            user = User.objects.get(pk=user_id)

            # Отмена основной регистрации
            if registration := Registration.objects.filter(event=event, user=user).first():
                registration.delete()
                _promote_from_waitlist(event)  # Перемещаем первого из листа ожидания
                return "registration_canceled"

            # Отмена записи в листе ожидания
            if waitlist_item := Waitlist.objects.filter(event=event, user=user).first():
                waitlist_item.delete()
                _update_waitlist_positions(event)  # Обновляем позиции
                return "waitlist_canceled"

            return "not_registered"

    except Exception as e:
        raise e


def _promote_from_waitlist(event: Event) -> None:
    """Перемещает первого из листа ожидания в основную регистрацию"""
    if first := Waitlist.objects.filter(event=event).order_by('position').first():
        Registration.objects.create(
            event=event,
            user=first.user,
            seat_number=Event.get_next_seat_number(event)
        )
        first.delete()
        _update_waitlist_positions(event)


def _update_waitlist_positions(event: Event) -> None:
    """Обновляет позиции в листе ожидания"""
    waitlist_items = Waitlist.objects.filter(event=event).order_by('position')
    for new_position, item in enumerate(waitlist_items, start=1):
        if item.position != new_position:
            item.position = new_position
            item.save(update_fields=['position'])