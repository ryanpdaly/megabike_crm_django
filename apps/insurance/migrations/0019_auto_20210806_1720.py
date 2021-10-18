# Generated by Django 3.1.4 on 2021-08-06 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0018_auto_20210726_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schadensmeldungstatus',
            name='status',
            field=models.CharField(choices=[('kv', 'KV eingereicht'), ('kvf', 'KV freigegeben'), ('re', 'Rechnung eingereicht'), ('be', 'Bezahlt'), ('azr', 'Abzurechnen'), ('ab', 'Abgelehnt')], max_length=3),
        ),
    ]
