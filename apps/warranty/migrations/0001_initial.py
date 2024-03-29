# Generated by Django 3.1.4 on 2021-02-15 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReklaTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('offen', 'Offen'), ('gemeldet', 'Beim Hersteller gemeldet'), ('eingeschickt', 'Zum Hersteller eingeschickt'), ('wartet', 'Wartet auf bearbeitung beim Hersteller'), ('eingetroffen', 'Ersatz eingetroffen'), ('montage', 'Wartet auf Montage'), ('abholbereit', 'Abholbereit'), ('abgelehnt', 'vom Hersteller abgelehnt'), ('erledigt', 'Erledit')], max_length=20)),
                ('sachbearbeiter', models.CharField(choices=[('12', 'Beskowski'), ('34', 'Wegener'), ('59', 'Daly'), ('61', 'Betke'), ('65', 'Bachmann'), ('68', 'Duhme'), ('70', 'Nolte'), ('72', 'Korpilla')], max_length=2)),
                ('date_created', models.DateField()),
                ('hersteller', models.CharField(max_length=30)),
                ('artikelnr', models.CharField(max_length=30)),
                ('bezeichnung', models.CharField(max_length=50)),
                ('menge', models.IntegerField()),
                ('auftragsnr', models.CharField(max_length=10)),
                ('fehlerbeschreibung', models.TextField()),
                ('kunde', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
    ]
