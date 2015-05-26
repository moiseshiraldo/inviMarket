# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0028_auto_20150526_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 26, 16, 10, 12, 131923, tzinfo=utc)),
        ),
    ]
