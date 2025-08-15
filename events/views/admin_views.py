""" Представления для администратора"""
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from ..forms import EventTemplateForm, EventForm, UserPermissionsForm
from ..models import EventTemplate, Event, User


# Декораторы для проверки полномочий
def is_admin(user):
    return user.is_staff

def dashboard_permission_required(view_func=None, permissions=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.is_superuser or u.dashboard_access),
        login_url='admin:login'
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

# Административный Дашборд
@staff_member_required
@dashboard_permission_required
def admin_dashboard(request):
    # Очистка сообщений если это не редирект от block/unblock
    if request.method == 'GET' and not request.GET.get('processed'):
        system_messages = messages.get_messages(request)
        for _ in system_messages:
            pass  # Очищаем все сообщения

    # Фильтрация пользователей
    username_filter = request.GET.get('username', '')
    users_query = User.objects.all().order_by('username')
    if username_filter:
        users_query = users_query.filter(username__icontains=username_filter)

    # Пагинация
    users_paginator = Paginator(users_query, 10)  # 10 пользователей на страницу
    users_page = users_paginator.get_page(request.GET.get('users_page'))

    events_paginator = Paginator(Event.objects.filter(is_active=True).order_by('date'), 10)  # 10 событий на страницу
    events_page = events_paginator.get_page(request.GET.get('events_page'))

    context = {
        'events_page': events_page,
        'users_page': users_page
    }
    return render(request, 'admin/dashboard.html', context)
#Создание шаблона
@user_passes_test(is_admin)
def create_template(request):
    if request.method == 'POST':
        form = EventTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('template_list')
    else:
        form = EventTemplateForm()

    return render(request, 'admin/create_template.html', {'form': form})


@user_passes_test(is_admin)
def template_list(request):
    templates = EventTemplate.objects.all()
    return render(request, 'admin/templates_list.html', {'templates': templates})

#Создание события
@user_passes_test(is_admin)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EventForm()

    return render(request, 'admin/create_event.html', {'form': form})

# Блокировка пользователя
@user_passes_test(is_admin)
def block_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.is_blocked = True
        user.save()
        return HttpResponseRedirect(f"{reverse('admin_dashboard')}?processed=1")  # Добавляем флаг

# Разблокировка пользователя
@user_passes_test(is_admin)
def unblock_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.is_blocked = False
        user.save()
        return HttpResponseRedirect(f"{reverse('admin_dashboard')}?processed=1")  # Добавляем флаг

# Изменение прав доступа
@user_passes_test(is_admin)
def edit_user_permissions(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = UserPermissionsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User permissions updated successfully')
            return redirect('admin_dashboard')
    else:
        form = UserPermissionsForm(instance=user)

    context = {
        'form': form,
        'user': request.user,  # Это ключевое изменение - передаём текущего пользователя
        'edited_user': user,  # Переименовываем user объекта для редактирования
        'title': 'Редактирование прав',
        'has_full_access': request.user.is_superuser or any([
            request.user.dashboard_access,
            request.user.can_manage_events,
            request.user.can_manage_templates,
            request.user.can_manage_users
        ]),
    }

    return render(request, 'admin/edit_permissions.html', context)