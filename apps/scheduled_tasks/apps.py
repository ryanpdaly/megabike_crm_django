from django.apps import AppConfig


class ScheduledTasksConfig(AppConfig):
    name = 'scheduled_tasks'

    def ready(self):
        from . import runapscheduler
        
