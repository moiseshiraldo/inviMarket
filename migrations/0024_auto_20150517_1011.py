# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0023_auto_20150517_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 17, 10, 11, 19, 850930, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'EC', 'E-commerce'), (b'GEN', 'Generic'), (b'MMD', 'Multimedia'), (b'RE', 'Referral'), (b'TEL', 'Telecommunications')]),
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='lang',
            field=models.CharField(max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English'), (b'multi', 'Multi-language')]),
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='webType',
            field=models.CharField(max_length=3, choices=[(b'APP', 'Application'), (b'CS', 'Cloud Service'), (b'DD', 'Direct Download'), (b'FO', 'Forum'), (b'PTC', 'Paid-To-Click'), (b'P2P', 'Peer to peer'), (b'ST', 'Streaming'), (b'TR', 'Tracker')]),
        ),
        migrations.AlterField(
            model_name='website',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'EC', 'E-commerce'), (b'GEN', 'Generic'), (b'MMD', 'Multimedia'), (b'RE', 'Referral'), (b'TEL', 'Telecommunications')]),
        ),
        migrations.AlterField(
            model_name='website',
            name='webType',
            field=models.CharField(max_length=3, choices=[(b'APP', 'Application'), (b'CS', 'Cloud Service'), (b'DD', 'Direct Download'), (b'FO', 'Forum'), (b'PTC', 'Paid-To-Click'), (b'P2P', 'Peer to peer'), (b'ST', 'Streaming'), (b'TR', 'Tracker')]),
        ),
    ]
