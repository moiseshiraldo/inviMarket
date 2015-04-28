# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0014_auto_20150406_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 6, 18, 49, 6, 295964, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
