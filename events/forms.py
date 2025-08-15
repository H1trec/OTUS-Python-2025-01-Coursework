from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import EventTemplate, Event, User
from django.utils.translation import gettext_lazy as _

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class EventTemplateForm(forms.ModelForm):
    class Meta:
        model = EventTemplate
        fields = ['name', 'description']

class EventForm(forms.ModelForm):
    date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date'},
            time_attrs={'type': 'time', 'step': '900'}  # Шаг 15 минут
        ),
        label=_("Дата и время")
    )

    class Meta:
        model = Event
        fields = ['date', 'template', 'max_seats', 'max_waitlist']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class EventRegistrationForm(forms.Form):
    pass

class UserPermissionsForm(forms.ModelForm):
    """Класс для управления доступом"""
    class Meta:
        model = User
        fields = [
            'is_staff',
            'is_superuser',
            'dashboard_access',
            'can_manage_events',
            'can_manage_templates',
            'can_manage_users'
        ]
        widgets = {
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dashboard_access': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_events': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_templates': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_users': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_staff': 'Работник',
            'is_superuser': 'Администратор',
            'dashboard_access': 'Доступ к панели управления',
            'can_manage_events': 'Управление событиями',
            'can_manage_templates': 'Управление шаблонами',
            'can_manage_users': 'Управление пользователями',
        }
