# Generated by Django 3.1.5 on 2021-02-14 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20210214_1718'),
        ('insurance', '0004_auto_20210214_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assonainfo',
            name='bike',
        ),
        migrations.AlterField(
            model_name='assonainfo',
            name='rahmennummer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.bike', to_field='rahmennummer'),
        ),
    ]
