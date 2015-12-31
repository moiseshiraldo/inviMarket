# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0002_auto_20150605_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteedition',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'CUL', 'Culture'), (b'EC', 'E-commerce'), (b'GEN', 'Generic'), (b'KNO', 'Knowledge'), (b'MMD', 'Multimedia'), (b'RE', 'Referral'), (b'TEL', 'Telecommunications')]),
        ),
        migrations.AlterField(
            model_name='website',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'CUL', 'Culture'), (b'EC', 'E-commerce'), (b'GEN', 'Generic'), (b'KNO', 'Knowledge'), (b'MMD', 'Multimedia'), (b'RE', 'Referral'), (b'TEL', 'Telecommunications')]),
        ),
    ]
