# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inviMarket', '0008_auto_20150313_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 3, 14, 20, 56, 0, 738672, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(related_name='receptor', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=b'static/users', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='website',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'static/sites'),
            preserve_default=True,
        ),
    ]
