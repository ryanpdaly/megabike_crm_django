# Generated by Django 3.1.4 on 2021-10-08 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0020_auto_20210922_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schadensmeldungstatus',
            name='status',
            field=models.CharField(choices=[('kv', 'KV eingereicht'), ('kvf', 'KV freigegeben'), ('re', 'Rechnung eingereicht'), ('nb', 'In Nachbearbeitung'), ('azr', 'Abzurechnen'), ('rs', 'Restsumme offen'), ('be', 'Bezahlt'), ('ab', 'Abgelehnt')], max_length=3),
        ),
    ]
