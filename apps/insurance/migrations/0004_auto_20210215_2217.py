# Generated by Django 3.1.5 on 2021-02-15 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0003_auto_20210215_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assonainfo',
            name='versicherungskarte',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='bikeleasinginfo',
            name='versicherungskarte',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='businessbikeinfo',
            name='versicherungskarte',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='enrainfo',
            name='versicherungskarte',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='euroradinfo',
            name='versicherungskarte',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
