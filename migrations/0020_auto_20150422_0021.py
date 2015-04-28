# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0019_auto_20150416_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='email_domain',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='website',
            name='lang',
            field=models.CharField(blank=True, max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English'), (b'multi', 'Multi-language')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='description',
            name='lang',
            field=models.CharField(blank=True, max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English'), (b'multi', 'Multi-language')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='lang',
            field=models.CharField(blank=True, max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English'), (b'multi', 'Multi-language')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='lang',
            field=models.CharField(max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English'), (b'multi', 'Multi-language')]),
            preserve_default=True,
        ),
    ]
