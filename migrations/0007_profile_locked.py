# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0006_auto_20150214_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='locked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
