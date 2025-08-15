""" Утилита для работы с БД """
from sqlalchemy import create_engine
from redis import Redis
from django.conf import settings

def get_sqlalchemy_engine():
    db = settings.DATABASES['default']
    return create_engine(
        f"postgresql://{db['USER']}:{db['PASSWORD']}@{db['HOST']}:{db['PORT']}/{db['NAME']}"
    )

def get_redis_connection():
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD or None,
        decode_responses=True
    )