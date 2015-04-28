# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inviMarket', '0009_auto_20150314_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='warnings',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='website',
            name='editors',
            field=models.ManyToManyField(related_name='edited_sites', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='website',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(related_name='sent_notification', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trade',
            name='proposer',
            field=models.ForeignKey(related_name='proposed_trade', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trade',
            name='receptor',
            field=models.ForeignKey(related_name='received_trade', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
