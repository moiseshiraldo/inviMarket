# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0010_auto_20150316_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='donation',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
