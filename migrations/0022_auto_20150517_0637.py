# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0021_auto_20150425_0010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='warnings',
        ),
        migrations.RemoveField(
            model_name='website',
            name='editors',
        ),
        migrations.AddField(
            model_name='siteedition',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='description',
            name='lang',
            field=models.CharField(blank=True, max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lang',
            field=models.CharField(blank=True, max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 17, 6, 37, 31, 441813, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='rating',
            field=models.PositiveSmallIntegerField(default=35),
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'GEN', 'Generic'), (b'MMD', 'Multimedia'), (b'COM', 'E-commerce'), (b'RE', 'Referral')]),
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='lang',
            field=models.CharField(max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English')]),
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='user',
            field=models.ForeignKey(related_name='editions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='webType',
            field=models.CharField(max_length=3, choices=[(b'FO', 'Forum'), (b'TR', 'Tracker'), (b'DD', 'Direct Download'), (b'ST', 'Streaming'), (b'CS', 'Cloud Service'), (b'PTC', 'Paid-To-Click'), (b'P2P', 'Peer to peer')]),
        ),
        migrations.AlterField(
            model_name='website',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'GEN', 'Generic'), (b'MMD', 'Multimedia'), (b'COM', 'E-commerce'), (b'RE', 'Referral')]),
        ),
        migrations.AlterField(
            model_name='website',
            name='webType',
            field=models.CharField(max_length=3, choices=[(b'FO', 'Forum'), (b'TR', 'Tracker'), (b'DD', 'Direct Download'), (b'ST', 'Streaming'), (b'CS', 'Cloud Service'), (b'PTC', 'Paid-To-Click'), (b'P2P', 'Peer to peer')]),
        ),
    ]
