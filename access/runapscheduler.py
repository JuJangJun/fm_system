# access/runapscheduler.py

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from apscheduler.triggers.cron import CronTrigger
from .views import check_and_save_to_slack
from django.conf import settings

logger = logging.getLogger(__name__)


def start():

    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default") 

    if not scheduler.get_job('check_and_save_to_slack'):  # check if job already exists
        scheduler.add_job(
            check_and_save_to_slack,
            # trigger=CronTrigger(minute='*/30'),  # 매 시간의 30분마다
            trigger=CronTrigger(second="0", minute="*"),  # 매 분(1분마다) 작동합니다. 
            id="check_and_save_to_slack",  # id는 고유해야합니다.
            max_instances=1,
            replace_existing=True,
        )
        
        logger.info("Added job 'check_and_save_to_slack'.")
    
    try:
        logger.info("Starting scheduler...")
        scheduler.start()

    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")


