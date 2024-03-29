# Generated by Django 3.1.5 on 2021-03-14 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0011_auto_20210308_2153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reklaticket',
            options={'permissions': ()},
        ),
        migrations.AlterField(
            model_name='reklastatusupdate',
            name='anmerkung',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reklastatusupdate',
            name='status',
            field=models.CharField(choices=[('offen', 'Offen'), ('gemeldet', 'Beim Hersteller gemeldet'), ('eingeschickt', 'Zum Hersteller eingeschickt'), ('wartet', 'Wartet auf bearbeitung beim Hersteller'), ('eingetroffen', 'Ersatz eingetroffen'), ('montage', 'Wartet auf Montage'), ('abholbereit', 'Abholbereit'), ('abgelehnt', 'vom Hersteller abgelehnt'), ('erledigt', 'Erledigt')], default='offen', max_length=20),
        ),
    ]
