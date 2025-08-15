### Курсовая работа на тему: «Сервис регистраций на event-события.»
Структура проекта:
```
EventsProject/
├── EventsProject/
│   ├── __init__.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── events/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── middleware.py
│   ├── forms.py 
│   ├── tasks.py 
│   ├── static/
│   │   └── styles.css
│   ├── services/
│   │   ├── __init__.py
│   │   ├── event_service.py
│   │   └── user_service.py
│   ├── templates/
│   │   ├── admin
│   │   │   ├── create_event.html
│   │   │   ├── create_template.html
│   │   │   ├── dashborad.html
│   │   │   ├── edit_permissions.html
│   │   │   └── templates_list.html
│   │   ├── events
│   │   │   ├── already_registered.html
│   │   │   ├── already_waitlisted.html
│   │   │   ├── cancel_regisrtation.html
│   │   │   ├── event_detail.html
│   │   │   ├── event_list.html
│   │   │   ├── register_event.html
│   │   │   ├── register_user.html
│   │   │   ├── user_profile.html
│   │   │   └── waitlisted.html
│   │   └── base.html
│   │
│   ├── views/
│   │   ├── __init__.py
│   │   ├── event_views.py
│   │   ├── user_views.py
│   │   └── admin_views.py
│   └── utils/
│       ├── __init__.py
│       ├── db.py 
│       └── exceptions.py
├── manage.py
└── requirements.txt
```
