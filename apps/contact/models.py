import datetime

from django.db import models

# Create your models here.

class PhoneContact(models.Model):
	date = models.DateField()

	ABTEILUNG_OPTIONS = (
		('werkstatt', 'Werkstatt'),
		('verkauf', 'Verkauf'),
		('buero', 'Büro'),
	)

	abteilung = models.CharField(max_length=15,
		choices = ABTEILUNG_OPTIONS,
	)

	STATUS_OPTIONS = (
		('offen', 'Offen'),
		('bearbeitung', 'In Bearbeitung'),
		('erledigt', 'Erledigt'),
	)

	status = models.CharField(max_length=15,
		choices=STATUS_OPTIONS,
		default='offen',
	)

	kundenname = models.CharField(max_length=30,)
	telefonnr = models.CharField(max_length=20,)
	anmerkungen = models.TextField()

	# Add this to a common list file?
	MITARBEITER_LIST = (
		('5', '5: B. Thürnau'),
		('12', '12: T. Beskowski'),
		('13', '13: J. Wienkötter'),
		('14', '14: T. Koesling'),
		('20', '20: K. Gorlov'),
		('21', '21: F. Hinderks'),
		('23', '23: A. Marutschke'),
		('28', '28: M. Wilholt'),
		('30', '30: T. Schweter'),
		('34', '34: F. Wegener'),
		('36', '36: S. Grotepaß'),
		('38', '38: R. Weiler'),
		('52', '52: S. Zietemann'),
		('56', '56: J. Wiholt'),
		('58', '58: V. Koncur'),
		('59', '59: R. Daly'),
		('60', '60: Hohendorf'),
		('61', '61: E. Betke'),
		('63', '63: C. Siebert'),
		('64', '64: L. Kurowski'),
		('65', '65: S. Bachmann'),
		('68', '68: L. Duhme'),
		('70', '70: F. Nolte'),
		('72', '72: R. Korpilla'),
		('73', '73: F. Stresemann'),
	)

	gesprochen_mit = models.CharField(max_length=32,
		choices = MITARBEITER_LIST,
	)

	def __str__(self):
		return f'{self.date}: {self.kundenname}'

	def save(self):
		if not self.id:
			self.date = datetime.date.today()
		super(PhoneContact, self).save()