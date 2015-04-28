# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0018_auto_20150411_2035'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trade',
            old_name='offer',
            new_name='offers',
        ),
        migrations.RenameField(
            model_name='trade',
            old_name='request',
            new_name='requests',
        ),
        migrations.RenameField(
            model_name='website',
            old_name='user',
            new_name='author',
        ),
        migrations.AlterField(
            model_name='chain',
            name='password',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='link',
            name='next_link',
            field=models.ForeignKey(related_name='previous_link', blank=True, to='inviMarket.Link', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='link',
            name='source_link',
            field=models.ForeignKey(related_name='children_links', blank=True, to='inviMarket.Link', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trade',
            name='proposer',
            field=models.ForeignKey(related_name='proposed_trades', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trade',
            name='receptor',
            field=models.ForeignKey(related_name='received_trades', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
