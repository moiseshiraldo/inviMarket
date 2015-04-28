# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0007_profile_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'/static/sites'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='website',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'/static/sites'),
            preserve_default=True,
        ),
    ]
