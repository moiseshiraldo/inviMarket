# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0002_auto_20141226_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'cars'),
            preserve_default=True,
        ),
    ]
