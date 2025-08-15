from django.shortcuts import redirect
from django.urls import reverse


class DashboardAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/dashboard/') and not request.user.is_authenticated:
            return redirect(reverse('login') + f'?next={request.path}')

        if request.path.startswith('/dashboard/') and not (
                request.user.is_superuser or
                request.user.dashboard_access
        ):
            return redirect('admin:index')

        return self.get_response(request)