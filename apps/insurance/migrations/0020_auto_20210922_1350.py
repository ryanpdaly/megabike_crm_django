# Generated by Django 3.1.5 on 2021-09-22 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0019_auto_20210806_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='schadensmeldung',
            name='bearbeiter',
            field=models.CharField(choices=[('5', '5: B. Thürnau'), ('12', '12: T. Beskowski'), ('13', '13: J. Wienkötter'), ('14', '14: T. Koesling'), ('20', '20: K. Gorlov'), ('21', '21: F. Hinderks'), ('23', '23: A. Marutschke'), ('28', '28: M. Wilholt'), ('30', '30: T. Schweter'), ('34', '34: F. Wegener'), ('36', '36: S. Grotepaß'), ('38', '38: R. Weiler'), ('52', '52: S. Zietemann'), ('56', '56: J. Wiholt'), ('57', '57: F. Boll'), ('58', '58: V. Koncur'), ('59', '59: R. Daly'), ('60', '60: Hohendorf'), ('61', '61: E. Betke'), ('63', '63: C. Siebert'), ('64', '64: L. Kurowski'), ('65', '65: S. Bachmann'), ('68', '68: L. Duhme'), ('70', '70: F. Nolte'), ('72', '72: R. Korpilla'), ('73', '73: F. Stresemann'), ('74', '74: R. Ramming'), ('75', '75: C. Malzahn'), ('76', '76: M. Feige')], default='59', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schadensmeldung',
            name='zahlungsreferenz',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='schadensmeldungfile',
            name='bearbeiter',
            field=models.CharField(choices=[('5', '5: B. Thürnau'), ('12', '12: T. Beskowski'), ('13', '13: J. Wienkötter'), ('14', '14: T. Koesling'), ('20', '20: K. Gorlov'), ('21', '21: F. Hinderks'), ('23', '23: A. Marutschke'), ('28', '28: M. Wilholt'), ('30', '30: T. Schweter'), ('34', '34: F. Wegener'), ('36', '36: S. Grotepaß'), ('38', '38: R. Weiler'), ('52', '52: S. Zietemann'), ('56', '56: J. Wiholt'), ('57', '57: F. Boll'), ('58', '58: V. Koncur'), ('59', '59: R. Daly'), ('60', '60: Hohendorf'), ('61', '61: E. Betke'), ('63', '63: C. Siebert'), ('64', '64: L. Kurowski'), ('65', '65: S. Bachmann'), ('68', '68: L. Duhme'), ('70', '70: F. Nolte'), ('72', '72: R. Korpilla'), ('73', '73: F. Stresemann'), ('74', '74: R. Ramming'), ('75', '75: C. Malzahn'), ('76', '76: M. Feige')], default='59', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schadensmeldungstatus',
            name='bearbeiter',
            field=models.CharField(choices=[('5', '5: B. Thürnau'), ('12', '12: T. Beskowski'), ('13', '13: J. Wienkötter'), ('14', '14: T. Koesling'), ('20', '20: K. Gorlov'), ('21', '21: F. Hinderks'), ('23', '23: A. Marutschke'), ('28', '28: M. Wilholt'), ('30', '30: T. Schweter'), ('34', '34: F. Wegener'), ('36', '36: S. Grotepaß'), ('38', '38: R. Weiler'), ('52', '52: S. Zietemann'), ('56', '56: J. Wiholt'), ('57', '57: F. Boll'), ('58', '58: V. Koncur'), ('59', '59: R. Daly'), ('60', '60: Hohendorf'), ('61', '61: E. Betke'), ('63', '63: C. Siebert'), ('64', '64: L. Kurowski'), ('65', '65: S. Bachmann'), ('68', '68: L. Duhme'), ('70', '70: F. Nolte'), ('72', '72: R. Korpilla'), ('73', '73: F. Stresemann'), ('74', '74: R. Ramming'), ('75', '75: C. Malzahn'), ('76', '76: M. Feige')], default='59', max_length=32),
            preserve_default=False,
        ),
    ]
