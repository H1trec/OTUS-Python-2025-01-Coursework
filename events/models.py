from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging

from events.utils.exceptions import UserBlocked, PastDateError

logger = logging.getLogger(__name__)

class User(AbstractUser):
    is_blocked = models.BooleanField(
        default=False,
        verbose_name=_('Blocked status'),
        help_text=_('Указывает заблокирована ли возможность регистрации на события для пользователя')
    )
    dashboard_access = models.BooleanField(
        default=False,
        verbose_name='Dashboard Access'
    )
    can_manage_events = models.BooleanField(
        default=False,
        verbose_name='Can manage events'
    )
    can_manage_templates = models.BooleanField(
        default=False,
        verbose_name='Can manage templates'
    )
    can_manage_users = models.BooleanField(
        default=False,
        verbose_name='Can manage users'
    )

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    @property
    def active_registrations(self):
        
        return self.user_registrations.filter(event__date__gte=timezone.now())

    @property
    def active_waitlists(self):
        
        return self.user_waitlists.filter(event__date__gte=timezone.now())

class EventTemplate(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Название шаблона")
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        blank=True
    )
    default_max_seats = models.PositiveIntegerField(
        default=settings.DEFAULT_MAX_SEATS,
        verbose_name=_("Количество мест")
    )
    default_max_waitlist = models.PositiveIntegerField(
        default=settings.DEFAULT_MAX_WAITLIST,
        verbose_name=_("Размер списка ожидания")
    )

    class Meta:
        db_table = 'event_templates'
        verbose_name = _('Event Template')
        verbose_name_plural = _('Event Templates')
        ordering = ['name']

    def __str__(self):
        return self.name

class Event(models.Model):
    """Класс описывающий событие"""
    date = models.DateTimeField(
        verbose_name=_("Дата и время"),
        db_index=True
    )
    template = models.ForeignKey(
        EventTemplate,
        on_delete=models.PROTECT,
        related_name='events',
        verbose_name=_("Шаблон")
    )
    max_seats = models.PositiveIntegerField(
        verbose_name=_("Количество мест"),
        help_text=_("Максимальное количество участников")
    )
    max_waitlist = models.PositiveIntegerField(
        verbose_name=_("Лист ожидания"),
        help_text=_("Максимальное количество участников в листе ожидания")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Статус"),
        help_text=_("Доступно ли мероприятие для регистрации")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Создано")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Изменено")
    )

    class Meta:
        db_table = 'events'
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['date']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.template.name} - {self.date.strftime('%d.%m.%Y')}"

    def clean(self):
        """Проверка на корректность перед сохранением"""
        if self.date < timezone.now():
            raise ValidationError("Дата события не может быть в прошлом")
        if self.max_seats < 1:
            raise ValidationError("Максимальное количество мест должно быть больше 1")
        if self.max_waitlist < 0:
            raise ValidationError("Количество мест в листе ожидания  не может меньше 0")

    @property
    def registered_count(self):
        """Количество зарегистрированных"""
        return self.event_registrations.count()

    @property
    def waitlist_count(self):
        """Количество в списке ожидания"""
        return self.event_waitlists.count()

    @property
    def available_seats(self):
        """Количество свободных мест"""
        return self.max_seats - self.registered_count

    @property
    def available_waitlist(self):
        """Количество свободных мест в листе ожидания"""
        return self.max_waitlist - self.waitlist_count

    @property
    def is_full(self):
        """Проверка наличия мест"""
        return self.available_seats <= 0 and self.available_waitlist <= 0

    def get_next_seat_number(self):
        """Получение следующего места"""
        last_reg = self.event_registrations.order_by('-seat_number').first()
        return last_reg.seat_number + 1 if last_reg else 1

    def get_next_waitlist_position(self):
        """Получение следующего места в листе ожидания"""
        last_wait = self.event_waitlists.order_by('-position').first()
        return last_wait.position + 1 if last_wait else 1

class Registration(models.Model):
    """Класс для регистрации"""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_registrations'
    )
    seat_number = models.PositiveIntegerField(
        verbose_name=_("Seat Number")
    )
    registered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Registration Time")
    )

    class Meta:
        db_table = 'registrations'
        unique_together = [('event', 'seat_number'), ('event', 'user')]
        ordering = ['seat_number']
        indexes = [
            models.Index(fields=['registered_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event} (Seat {self.seat_number})"

    def clean(self):
        """Проверка перед сохранением"""
        if self.event.date < timezone.now():
            raise PastDateError()
        if self.user.is_blocked:
            raise UserBlocked()

class Waitlist(models.Model):
    """Класс для листа ожидания"""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_waitlists'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_waitlists'
    )
    position = models.PositiveIntegerField(
        verbose_name=_("Waitlist Position")
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Join Time")
    )

    class Meta:
        db_table = 'waitlists'
        unique_together = [('event', 'user'), ('event', 'position')]
        ordering = ['position']
        indexes = [
            models.Index(fields=['joined_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event} (Position {self.position})"

    def clean(self):
        """Проверка перед сохранением"""
        if self.event.date < timezone.now():
            raise PastDateError()
        if self.user.is_blocked:
            raise UserBlocked()
        if Registration.objects.filter(event=self.event, user=self.user).exists():

            raise ValidationError("Вы уже заргистрированы на событие")
