import os
from celery import Celery


# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EventsProject.settings')

app = Celery('EventsProject')  # Используем имя вашего конфига

# Используем settings из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоподгрузка задач из всех зарегистрированных приложений
app.autodiscover_tasks()