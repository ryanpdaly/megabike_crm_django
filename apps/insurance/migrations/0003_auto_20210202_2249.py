# Generated by Django 3.1.5 on 2021-02-02 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0002_auto_20210108_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bikeleasinginfo',
            name='fahrzeug',
        ),
        migrations.RemoveField(
            model_name='bikeleasinginfo',
            name='kundennummer',
        ),
        migrations.RemoveField(
            model_name='bikeleasinginfo',
            name='nachname',
        ),
        migrations.RemoveField(
            model_name='businessbikeinfo',
            name='fahrzeug',
        ),
        migrations.RemoveField(
            model_name='businessbikeinfo',
            name='kundennummer',
        ),
        migrations.RemoveField(
            model_name='businessbikeinfo',
            name='nachname',
        ),
        migrations.RemoveField(
            model_name='enrainfo',
            name='fahrzeug',
        ),
        migrations.RemoveField(
            model_name='enrainfo',
            name='kundennummer',
        ),
        migrations.RemoveField(
            model_name='enrainfo',
            name='nachname',
        ),
        migrations.RemoveField(
            model_name='euroradinfo',
            name='fahrzeug',
        ),
        migrations.RemoveField(
            model_name='euroradinfo',
            name='kundennummer',
        ),
        migrations.RemoveField(
            model_name='euroradinfo',
            name='nachname',
        ),
        migrations.AddField(
            model_name='assonainfo',
            name='rahmennummer',
            field=models.CharField(default='NONEGIVEN', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bikeleasinginfo',
            name='leasingbank',
            field=models.CharField(choices=[('A', 'ALS Leasing GmbH'), ('H', 'Hofmann Leasing GmbH'), ('D', 'Digital Mobility Leasing GmbH')], max_length=1),
        ),
    ]
