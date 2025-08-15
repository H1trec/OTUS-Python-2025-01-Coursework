from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EventTemplate, Event, Registration, Waitlist


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Кастомная админка для управления доступом"""
    list_display = ('username', 'email', 'is_blocked', 'is_staff', 'dashboard_access',
                    'can_manage_events', 'can_manage_templates', 'can_manage_users')
    list_filter = ('is_blocked', 'is_staff', 'is_superuser', 'dashboard_access',
                   'can_manage_events', 'can_manage_templates', 'can_manage_users')
    list_editable = ('dashboard_access', 'can_manage_events', 'can_manage_templates', 'can_manage_users')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_blocked',
                'dashboard_access',
                'can_manage_events',
                'can_manage_templates',
                'can_manage_users',
                'groups',
                'user_permissions'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    filter_horizontal = ('groups', 'user_permissions',)

    actions = ['grant_full_dashboard_access', 'revoke_all_dashboard_permissions',
               'grant_dashboard_access', 'revoke_dashboard_access']

    @admin.action(description="Grant full dashboard permissions")
    def grant_full_dashboard_access(self, request, queryset):
        queryset.update(
            dashboard_access=True,
            can_manage_events=True,
            can_manage_templates=True,
            can_manage_users=True
        )

    @admin.action(description="Revoke all dashboard permissions")
    def revoke_all_dashboard_permissions(self, request, queryset):
        queryset.update(
            dashboard_access=False,
            can_manage_events=False,
            can_manage_templates=False,
            can_manage_users=False
        )

    @admin.action(description="Дать доступ к Dashboard")
    def grant_dashboard_access(self, request, queryset):
        queryset.update(dashboard_access=True)

    @admin.action(description="Забрать доступ к Dashboard")
    def revoke_dashboard_access(self, request, queryset):
        queryset.update(dashboard_access=False)

    def get_urls(self):
        urls = super().get_urls()
        return urls


@admin.register(EventTemplate)
class EventTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('template', 'date', 'max_seats', 'max_waitlist', 'registrations_count', 'waitlist_count')
    list_filter = ('date', 'template')
    date_hierarchy = 'date'
    ordering = ('-date',)

    def registrations_count(self, obj):
        return obj.event_registrations.count()

    registrations_count.short_description = 'Registrations'

    def waitlist_count(self, obj):
        return obj.event_waitlists.count()

    waitlist_count.short_description = 'Waitlist'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'seat_number')
    list_filter = ('event',)
    raw_id_fields = ('user',)
    search_fields = ('user__username', 'event__template__name')


@admin.register(Waitlist)
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'position')
    list_filter = ('event',)
    raw_id_fields = ('user',)
    search_fields = ('user__username', 'event__template__name')