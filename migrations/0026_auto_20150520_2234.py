# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0025_auto_20150520_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 20, 22, 34, 5, 990971, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='website',
            name='name',
            field=models.CharField(unique=True, max_length=20, db_index=True),
        ),
    ]
