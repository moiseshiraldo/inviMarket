# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0004_auto_20150105_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='notify',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
