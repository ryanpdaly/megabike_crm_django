# Generated by Django 3.1.4 on 2021-04-20 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_auto_20210418_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonecontact',
            name='abteilung',
            field=models.CharField(choices=[('werkstatt', 'Werkstatt'), ('verkauf', 'Verkauf'), ('buero', 'Büro'), ('neurad', 'Neuräder')], max_length=15),
        ),
    ]
