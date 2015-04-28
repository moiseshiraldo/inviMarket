# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import inviMarket.models


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0011_trade_donation'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteedition',
            name='comments',
            field=models.TextField(max_length=400, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=inviMarket.models.avatar_file_name, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='lang',
            field=models.CharField(max_length=5, choices=[(b'es', b'Espa\xc3\xb1ol'), (b'en', b'English')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='site',
            field=models.ForeignKey(blank=True, to='inviMarket.Website', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='source',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
