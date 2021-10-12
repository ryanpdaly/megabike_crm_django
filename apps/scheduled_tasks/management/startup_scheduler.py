import datetime
import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites import shortcuts
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore

import apps.insurance.models as insurance_models


# TODO: This logger doesn't actually seem to work?
logger = logging.getLogger(__name__)


def email_faellig_versicherung():
	# TODO: We end up using this date in a couple places and redefine it every time. Set in settings/local_settings?
	faellig_date = (datetime.datetime.today() - datetime.timedelta(days=7)).date()
	schaden_list = insurance_models.Schadensmeldung.objects.all()
	logging.info(schaden_list)

	for schaden in schaden_list:
		current_status = insurance_models.SchadensmeldungStatus.objects.filter(schadensmeldung=schaden).order_by('-id')[0]
		is_faellig = current_status.date <= faellig_date
		is_erledigt = current_status.status in ['be', 'ab', ]

		if is_erledigt is True or is_faellig is False:
			schaden_list = schaden_list.exclude(pk=schaden.pk)

		# TODO: Figure out how to add domain to our url.
		# domain = 'localhost:8000/'
		domain = shortcuts.get_current_site()
		schaden.url = f'{domain}{reverse("insurance:schaden-detail", kwargs={"pk":schaden.id,})}'

	context = {
		'ticket_list': schaden_list,
		'date': datetime.date.today(),
		'domain': settings.DEFAULT_DOMAIN,
	}

	msg_html = render_to_string(
		f'scheduled_tasks/insurance_faellig.html',
		context=context,
	)

	# TODO: Set recipients using variable in local_settings before production
	send_mail(
		f'Insgesamt {schaden_list.count()} fällige Versicherungsfälle',
		'',
		'megabikeCRM@gmail.com',
		['megabikeCRM@gmail.com'],
		fail_silently=False,
		html_message=msg_html
		)
	logger.info("Email sent")


scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), 'default')
logger.info("Scheduler instance created")


# TODO: This runs every single time that manage.py is called, not just when server running
def start():
	logger.info("Starting scheduler")
	logging.basicConfig()
	if settings.DEBUG:
		# Hook into the apscheduler logger
		logging.getLogger('apscheduler').setLevel(logging.INFO)
	else:
		logging.getLogger('apscheduler').setLevel(logging.WARNING)

	# TODO: Set schedule to once weekly before deployment
	scheduler.add_job(
		email_faellig_versicherung,
		# jobstore='djangojobstore',
		trigger=CronTrigger(minute="*/1"),
		id="insurance_email",
		max_instances=1,
		replace_existing=True
	)

	# TODO: This causes gitbash to hang and become non-responsive
	"""
	try:
		scheduler.start()
		logger.info("Scheduler started from AppConfig...")
	except KeyboardInterrupt:
		logger.info("Stopping scheduler...")
		scheduler.shutdown()
		logger.info("Scheduler shutdown sucessfully.")
	"""
	scheduler.start()
