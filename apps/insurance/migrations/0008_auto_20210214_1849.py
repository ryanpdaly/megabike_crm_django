# Generated by Django 3.1.5 on 2021-02-14 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20210214_1718'),
        ('insurance', '0007_auto_20210214_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikeleasinginfo',
            name='rahmennummer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.bike'),
        ),
    ]
