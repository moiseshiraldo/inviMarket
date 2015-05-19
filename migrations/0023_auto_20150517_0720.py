# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0022_auto_20150517_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteedition',
            name='email_domain',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='siteedition',
            name='refvalidator',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 17, 7, 20, 24, 251594, tzinfo=utc)),
        ),
    ]
