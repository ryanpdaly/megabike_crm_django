# Generated by Django 3.1.4 on 2021-07-01 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0005_auto_20210308_2153'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schadensmeldung',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unternehmen', models.CharField(choices=[('as', 'Assona'), ('eu', 'Eurorad')], max_length=3)),
                ('schadensnummer', models.CharField(max_length=30)),
                ('kundennummer', models.IntegerField()),
                ('kundenname', models.CharField(max_length=30)),
                ('vorgangsnummer', models.CharField(max_length=10)),
                ('reparatur_datum', models.DateField(blank=True, null=True)),
                ('created', models.DateField()),
                ('updated', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='SchadensmeldungStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('kv', 'KV eingereicht'), ('kvf', 'KV freigegeben'), ('re', 'Rechnung eingereicht'), ('be', 'Bezahlt'), ('ab', 'Abgelehnt')], max_length=3)),
                ('anmerkung', models.TextField(blank=True)),
                ('schadensmeldung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.schadensmeldung')),
            ],
        ),
    ]