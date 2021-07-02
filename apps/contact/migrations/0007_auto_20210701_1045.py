# Generated by Django 3.1.4 on 2021-07-01 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_auto_20210420_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outgoingcall',
            name='anruf_von',
            field=models.CharField(choices=[('5', '5: B. Thürnau'), ('12', '12: T. Beskowski'), ('13', '13: J. Wienkötter'), ('14', '14: T. Koesling'), ('20', '20: K. Gorlov'), ('21', '21: F. Hinderks'), ('23', '23: A. Marutschke'), ('28', '28: M. Wilholt'), ('30', '30: T. Schweter'), ('34', '34: F. Wegener'), ('36', '36: S. Grotepaß'), ('38', '38: R. Weiler'), ('52', '52: S. Zietemann'), ('56', '56: J. Wiholt'), ('57', '57: F. Boll'), ('58', '58: V. Koncur'), ('59', '59: R. Daly'), ('60', '60: Hohendorf'), ('61', '61: E. Betke'), ('63', '63: C. Siebert'), ('64', '64: L. Kurowski'), ('65', '65: S. Bachmann'), ('68', '68: L. Duhme'), ('70', '70: F. Nolte'), ('72', '72: R. Korpilla'), ('73', '73: F. Stresemann')], max_length=32),
        ),
        migrations.AlterField(
            model_name='phonecontact',
            name='gesprochen_mit',
            field=models.CharField(choices=[('5', '5: B. Thürnau'), ('12', '12: T. Beskowski'), ('13', '13: J. Wienkötter'), ('14', '14: T. Koesling'), ('20', '20: K. Gorlov'), ('21', '21: F. Hinderks'), ('23', '23: A. Marutschke'), ('28', '28: M. Wilholt'), ('30', '30: T. Schweter'), ('34', '34: F. Wegener'), ('36', '36: S. Grotepaß'), ('38', '38: R. Weiler'), ('52', '52: S. Zietemann'), ('56', '56: J. Wiholt'), ('57', '57: F. Boll'), ('58', '58: V. Koncur'), ('59', '59: R. Daly'), ('60', '60: Hohendorf'), ('61', '61: E. Betke'), ('63', '63: C. Siebert'), ('64', '64: L. Kurowski'), ('65', '65: S. Bachmann'), ('68', '68: L. Duhme'), ('70', '70: F. Nolte'), ('72', '72: R. Korpilla'), ('73', '73: F. Stresemann')], max_length=32),
        ),
    ]
