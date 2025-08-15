### Курсовая работа на тему: «Сервис регистраций на event-события.»

В проекте реализован функционал регистрации на события. 
#### Структура проекта:
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
#### Основные модули

##### Стандартное ядро приложения
* admins.py - интеграция с Django Admin и реализация кастомной админки.  
* forms.py  - формы проекта: события, шаблоны, регистрация, управление доступом.
* models.py - модели проекта: пользватель, шаблн, событие, регистрация на событие, лист ожидания.

##### Представления  
* admin_views.py - представления для админки, создания шаблонов и событий, блокировки/разблокировки пользователей, управления доступом.
* event_views.py - представления для событий: список, детализация,регистрация и ее отмена.   
* user_views.py  - Представления для пользователей: профиль и регистрация в приложении.

##### Сервисы   
* event_service.py - логика создания событий, регистрации, управления очередями.  
* user_service.py  - логика регистрации пользователей, профили.
  
##### Утилиты  
* db.py         - настройки для обращения к БД.  
* exceptions.py - кастомные исключения.

##### Шаблоны

###### Административные  
* create_event.html     - создание события  
* create_template.html  - создание шаблона  
* edit_permissions.html - редактирование прав  
* dashborad.html        - кастомная админка  
* templates_list.html   - список событий  

###### Общие 
* already_registered.html  - вывод информации по событию, в случе если уже зарегистрирован  
* already_waitlisted.html  - вывод информации по событию, в случе если уже в списке ожидания  
* cancel_regisrtation.html - отмена регистрации  
* event_detail.html        - детали события  
* event_list.html          - список событий  
* register_event.html      - регистрация на событие  
* register_user.html       - регистрация в приложении  
* user_profile.html        - профиль пользователя  
* waitlisted.html          - список ожидания  

#### Реализованная логика  

#### Дальнейшее развитие
