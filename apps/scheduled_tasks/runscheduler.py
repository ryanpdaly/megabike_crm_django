import logging

from django.conf import settings
from django.conf import local_settings

from apscheduler.schedulers.bloacking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util


logger = logging.getLogger(__name__)

def email_faellig_versicherung():
	logger.info("Sending email")
	send_mail(
		'Test scheduled email',
		'This is a test scheduled email.',
		'megabikeCRM@gmail.com',
		INSURANCE_EMPLOYEES,
		fail_silently = False,
		)
	logger.info("Email sent")

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database. It helps to prevent the
    database from filling up with old historical records that are no longer useful.

    :param max_age: The maximum length of time to retain historical job execution records. Defaults
                    to 7 days.
    """
	DjangoJobExecution.objects.delete_old_job_executions(max_age)

"""
class Command(BaseCommand):
	help = "Runs APscheduler."

	def handle(self, *args, **options):
		scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
		scheduler.add_jobstore(DjangoJobStore(), "default")

		scheduler.add_job(
			email_faellig_versicherung,
			jobstore='djangojobstore',
			trigger=CronTrigger(minute="*/1"),	#Every minute
			id="example_email",
			max_instances = 1,
			replace_existing=True 
		)
		logger.info("Added job 'email_faellig_versicherung'.")

		try:
			logger.info("Starting scheduler...")
			scheduler.start()
		except KeyboardInterrupt:
			logger.info("Stopping scheduler...")
			scheduler.shutdown()
			logger.info("Scheduler shut down successfully!")
"""


scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
logger.info("Scheduler instance created")

def start():
	logger.info("Starting scheduler")
	if settings.DEBUG:
		# Hook into the apscheduler logger
		logging.basicConfig()
		logging.getLogger('apscheduler').setLevel(logging.DEBUG)

		scheduler.add_job(
			email_faellig_versicherung, 
			jobstore='djangojonstore',
			trigger=CronTrigger(minute="*/1"),
			id="insurance_email",
			max_instances = 1,
			replace_existing=True
		)

		scheduler.start()