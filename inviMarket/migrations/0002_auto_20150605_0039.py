# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteedition',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'CUL', 'Culture'), (b'EC', 'E-commerce'), (b'GEN', 'Generic'), (b'MMD', 'Multimedia'), (b'RE', 'Referral'), (b'TEL', 'Telecommunications')]),
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='webType',
            field=models.CharField(max_length=3, choices=[(b'APP', 'Application'), (b'CS', 'Cloud Service'), (b'CO', 'Community'), (b'DD', 'Direct Download'), (b'PTC', 'Paid-To-Click'), (b'P2P', 'Peer to peer'), (b'SN', 'Social network'), (b'ST', 'Streaming'), (b'TR', 'Tracker')]),
        ),
        migrations.AlterField(
            model_name='website',
            name='category',
            field=models.CharField(max_length=3, choices=[(b'CUL', 'Culture'), (b'EC', 'E-commerce'), (b'GEN', 'Generic'), (b'MMD', 'Multimedia'), (b'RE', 'Referral'), (b'TEL', 'Telecommunications')]),
        ),
        migrations.AlterField(
            model_name='website',
            name='webType',
            field=models.CharField(max_length=3, choices=[(b'APP', 'Application'), (b'CS', 'Cloud Service'), (b'CO', 'Community'), (b'DD', 'Direct Download'), (b'PTC', 'Paid-To-Click'), (b'P2P', 'Peer to peer'), (b'SN', 'Social network'), (b'ST', 'Streaming'), (b'TR', 'Tracker')]),
        ),
    ]
