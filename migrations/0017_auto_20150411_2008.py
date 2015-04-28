# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0016_auto_20150409_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chain',
            name='url_hash',
            field=models.CharField(max_length=60),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='link',
            name='source_link',
            field=models.ForeignKey(related_name='children_links', to='inviMarket.Link', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='key_expires',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
