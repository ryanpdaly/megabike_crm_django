# Generated by Django 3.1.4 on 2021-02-18 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0009_auto_20210217_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reklastatusupdate',
            name='status',
            field=models.CharField(choices=[('offen', 'Offen'), ('gemeldet', 'Beim Hersteller gemeldet'), ('eingeschickt', 'Zum Hersteller eingeschickt'), ('wartet', 'Wartet auf bearbeitung beim Hersteller'), ('eingetroffen', 'Ersatz eingetroffen'), ('montage', 'Wartet auf Montage'), ('abholbereit', 'Abholbereit'), ('abgelehnt', 'vom Hersteller abgelehnt'), ('erledigt', 'Erledigt')], max_length=20),
        ),
    ]