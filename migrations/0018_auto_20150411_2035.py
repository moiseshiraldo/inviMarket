# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0017_auto_20150411_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chain',
            name='password',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chain',
            name='url_hash',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
    ]
