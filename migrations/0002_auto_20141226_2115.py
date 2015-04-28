# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='siteedition',
            old_name='source_en',
            new_name='source',
        ),
        migrations.RemoveField(
            model_name='siteedition',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='siteedition',
            name='description_es',
        ),
        migrations.RemoveField(
            model_name='siteedition',
            name='protected',
        ),
        migrations.RemoveField(
            model_name='siteedition',
            name='source_es',
        ),
        migrations.AddField(
            model_name='siteedition',
            name='date',
            field=models.DateField(default=datetime.date(2014, 12, 26), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='siteedition',
            name='description',
            field=models.TextField(default='Description', max_length=5000, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='siteedition',
            name='site',
            field=models.ForeignKey(default=1, blank=True, to='inviMarket.Website'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='website',
            name='protected',
            field=models.BooleanField(default=False),
        ),
    ]
