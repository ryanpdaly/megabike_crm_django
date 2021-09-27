import logging

from django.apps import AppConfig


logger = logging.getLogger(__name__)

class ScheduledTasksConfig(AppConfig):
    name = 'scheduled_tasks'

    def ready(self):
        logger.WARNING("scheduled_tasks app ready")
        
        from . import runscheduler
        if settings.SCHEDULER_AUTOSTART:
            runscheduler.start()
        
