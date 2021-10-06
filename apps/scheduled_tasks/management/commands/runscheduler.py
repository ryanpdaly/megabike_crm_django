import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

logger = logging.getLogger(__name__)


# TODO: Refactor, this function is defined in two places
def email_faellig_versicherung():
	logger.info("Sending email")
	send_mail(
		'Test scheduled email',
		'This is a test scheduled email.',
		'megabikeCRM@gmail.com',
		['megabikeCRM@gmail.com'],
		fail_silently=False,
	)
	logger.info("Email sent")


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
	"""
	This job deletes APScheduler job execution entries older than 'max_age' from the database. It helps to prevent
	the database from filling up with old historical records that are no longer useful.

	:param max_age: The maximum length of time to retain historical job execution records. Defaults to 7 day.
	"""
	DjangoJobExecution.objects.delete_old_job_executions(max_age)

# This also runs at startup?
class Command(BaseCommand):
	help = "Runs APscheduler."

	def handle(self, *args, **options):
		myscheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
		myscheduler.add_jobstore(DjangoJobStore(), "default")
		"""
		myscheduler.add_job(
			email_faellig_versicherung,
			# jobstore='DjangoJobStore',
			trigger=CronTrigger(minute="*/1"),  # Every minute
			id="example_email",
			max_instances=1,
			replace_existing=True
		)
		"""
		logger.info("Added job 'email_faellig_versicherung'.")


		try:
			logger.info("Starting scheduler from command...")
			myscheduler.start()
		except KeyboardInterrupt:
			logger.info("Stopping scheduler...")
			myscheduler.shutdown()
			logger.info("Scheduler shut down successfully")
