# Generated by Django 3.1.4 on 2021-07-16 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0010_auto_20210716_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schadensmeldung',
            name='unternehmen',
            field=models.CharField(choices=[('as', 'Assona'), ('bu', 'Businessbike'), ('jo', 'JobRad'), ('le', 'Lease-a-Bike')], max_length=3),
        ),
    ]
