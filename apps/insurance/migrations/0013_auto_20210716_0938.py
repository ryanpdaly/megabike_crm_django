# Generated by Django 3.1.4 on 2021-07-16 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0012_auto_20210716_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schadensmeldung',
            name='unternehmen',
            field=models.CharField(choices=[('as', 'Assona'), ('bi', 'Bikeleasing-Service'), ('bu', 'Businessbike'), ('en', 'ENRA'), ('jo', 'JobRad'), ('le', 'Lease-a-Bike')], max_length=3),
        ),
    ]
