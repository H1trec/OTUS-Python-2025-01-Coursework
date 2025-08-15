"""
URL configuration for EventsProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
# from django.contrib import admin
from django.contrib import admin
from django.urls import path, include
from events.views.admin_views import admin_dashboard, create_template, template_list, create_event, block_user, unblock_user, edit_user_permissions
from events.views.event_views import event_list, event_detail, register_for_event_view, cancel_registration_view
from events.views.user_views import register_user, user_profile
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
   # Admin URLs
    path('admin/',admin.site.urls),
    path('dashboard/edit_permissions/<int:user_id>/', edit_user_permissions, name='edit_user_permissions'),
    path('dashboard/user/<int:user_id>/block/', block_user, name='block_user'),
    path('dashboard/user/<int:user_id>/unblock/', unblock_user, name='unblock_user'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('templates/create/', create_template, name='create_template'),
    path('events/create/', create_event, name='create_event'),
    path('templates/', template_list, name='template_list'),
    path('', event_list, name='home'),
    path('register/', register_user, name='register_user'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    path('events/<int:event_id>/register/', register_for_event_view, name='register_for_event'),
    path('events/<int:event_id>/cancel/', cancel_registration_view, name='cancel_registration'),
    path('events/', event_list, name='event_list'),
    path('login/', LoginView.as_view(template_name='events/register_user.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', user_profile, name='user_profile'),
]
