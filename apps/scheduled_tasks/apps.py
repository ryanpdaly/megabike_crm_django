import logging

from django.apps import AppConfig
from django.conf import settings


logger = logging.getLogger(__name__)


class ScheduledTasksConfig(AppConfig):
    name = 'apps.scheduled_tasks'

    def ready(self):
        logger.info("scheduled_tasks app ready")

        from apps.scheduled_tasks.management import startup_scheduler
        if settings.SCHEDULER_AUTOSTART:
            startup_scheduler.start()
        
