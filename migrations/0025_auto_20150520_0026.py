# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0024_auto_20150517_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_visit',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 20, 0, 26, 21, 811532, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='website',
            name='email_domain',
            field=models.CharField(db_index=True, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='name',
            field=models.CharField(max_length=20, db_index=True),
        ),
    ]
