import json
import os

from django.conf import settings


# FIXME: Nothing in here is really a model. Rename/relocate?

# FIXME: Where does this function even belong? Do I need a utils file?
def json_to_tuple_list(file_in):
	list_out = []

	with open(file_in, 'r', encoding="UTF-8") as file:
		dict_temp = json.load(file)

	for key, value in dict_temp.items():
		list_out.append((key, value))

	return list_out


# FIXME: Name this consistently? e.g. ABTEILUNGEN, MITARBEITER, LIEFERANTEN
ABTEILUNG_OPTIONS = (
	('werkstatt', 'Werkstatt'),
	('verkauf', 'Verkauf'),
	('buero', 'Büro'),
)

MITARBEITER_ALL = json_to_tuple_list(os.path.join(settings.BASE_DIR, 'local_lists/employees.json'))
LIEFERANTEN = json_to_tuple_list(os.path.join(settings.BASE_DIR, 'local_lists/distributors.json'))
