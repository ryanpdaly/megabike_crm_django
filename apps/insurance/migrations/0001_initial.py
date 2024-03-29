# Generated by Django 3.1.4 on 2021-02-15 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceCompanies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(choices=[('no', 'None'), ('as', 'Assona'), ('bl', 'Bikeleasing Service'), ('bu', 'Businessbike'), ('en', 'ENRA'), ('eu', 'Eurorad')], default='no', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='EuroradInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginn', models.DateField()),
                ('vertragsnummer', models.CharField(max_length=20)),
                ('rahmennummer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.bike', to_field='rahmennummer')),
            ],
        ),
        migrations.CreateModel(
            name='EnraInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginn', models.DateField()),
                ('policenummer', models.CharField(max_length=20)),
                ('versicherungskarte', models.FileField(blank=True, upload_to='')),
                ('rahmennummer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.bike', to_field='rahmennummer')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessbikeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginn', models.DateField()),
                ('ende', models.DateField()),
                ('policenummer', models.CharField(max_length=30)),
                ('paket', models.CharField(choices=[('D', 'Durchsicht'), ('I', 'Inspektion'), ('F', 'Full Service'), ('E', 'Instandhaltungs+ enthalten'), ('N', 'Instandhaltungs+ nicht enthalten')], max_length=30)),
                ('verschleiss_guthaben', models.BooleanField(default=False)),
                ('versicherungskarte', models.FileField(blank=True, upload_to='')),
                ('rahmennummer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.bike', to_field='rahmennummer')),
            ],
        ),
        migrations.CreateModel(
            name='BikeleasingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nutzer_id', models.CharField(max_length=20)),
                ('paket', models.CharField(choices=[('P', 'Premium'), ('P+', 'Premium Plus')], max_length=20)),
                ('inspektion', models.BooleanField()),
                ('leasingbank', models.CharField(choices=[('A', 'ALS Leasing GmbH'), ('H', 'Hofmann Leasing GmbH'), ('D', 'Digital Mobility Leasing GmbH')], max_length=1)),
                ('beginn', models.DateField()),
                ('versicherungskarte', models.FileField(blank=True, upload_to='')),
                ('rahmennummer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.bike', to_field='rahmennummer')),
            ],
        ),
        migrations.CreateModel(
            name='AssonaInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vertragsnummer', models.CharField(max_length=10)),
                ('beginn', models.DateField()),
                ('versicherungskarte', models.FileField(blank=True, upload_to='')),
                ('rahmennummer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.bike', to_field='rahmennummer')),
            ],
        ),
    ]
