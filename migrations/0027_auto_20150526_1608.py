# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0026_auto_20150520_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(related_name='sent_notification', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 26, 16, 8, 54, 43706, tzinfo=utc)),
        ),
    ]
