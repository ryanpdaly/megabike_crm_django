# Generated by Django 3.1.5 on 2021-03-08 20:53

import apps.warranty.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warranty', '0010_auto_20210219_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reklafile',
            name='file',
            field=models.FileField(upload_to=apps.warranty.models.set_path_and_rename),
        ),
    ]