# access/apps.py
## 스케줄러 관련 코드
from django.apps import AppConfig
from django.conf import settings


class AccessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'access'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import runapscheduler
            runapscheduler.start()


