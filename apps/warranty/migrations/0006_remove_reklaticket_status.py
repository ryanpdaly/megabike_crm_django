# Generated by Django 3.1.5 on 2021-02-17 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0005_auto_20210217_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reklaticket',
            name='status',
        ),
    ]
