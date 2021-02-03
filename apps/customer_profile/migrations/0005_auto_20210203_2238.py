# Generated by Django 3.1.5 on 2021-02-03 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_profile', '0004_auto_20210203_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='versicherungsunternehmen',
            field=models.CharField(choices=[('no', 'None'), ('as', 'Assona'), ('bl', 'Bikeleasing Service'), ('bu', 'Businessbike'), ('en', 'ENRA'), ('eu', 'Eurorad')], default='no', max_length=2),
        ),
    ]
