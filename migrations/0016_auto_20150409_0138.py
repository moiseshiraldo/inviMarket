# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inviMarket', '0015_profile_last_visit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chain',
            old_name='URLhash',
            new_name='url_hash',
        ),
        migrations.RemoveField(
            model_name='link',
            name='nextlink',
        ),
        migrations.RemoveField(
            model_name='link',
            name='offer',
        ),
        migrations.AddField(
            model_name='link',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 9, 1, 37, 22, 726380, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='link',
            name='last_link',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='next_link',
            field=models.ForeignKey(related_name='previous_link', to='inviMarket.Link', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='source_link',
            field=models.ForeignKey(related_name='children_links', default='', to='inviMarket.Link'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='link',
            name='user',
            field=models.ForeignKey(default='', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chain',
            name='password',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
    ]
