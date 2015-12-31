# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0003_auto_20150616_2330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trade',
            old_name='comments',
            new_name='proposer_comments',
        ),
        migrations.AddField(
            model_name='trade',
            name='receptor_comments',
            field=models.TextField(max_length=400, blank=True),
        ),
        migrations.AlterField(
            model_name='siteedition',
            name='webType',
            field=models.CharField(max_length=3, choices=[(b'APP', 'Application'), (b'CS', 'Cloud Service'), (b'CO', 'Community'), (b'DD', 'Direct Download'), (b'GA', 'Game'), (b'PTC', 'Paid-To-Click'), (b'P2P', 'Peer to peer'), (b'SN', 'Social network'), (b'ST', 'Streaming'), (b'TR', 'Tracker')]),
        ),
        migrations.AlterField(
            model_name='website',
            name='webType',
            field=models.CharField(max_length=3, choices=[(b'APP', 'Application'), (b'CS', 'Cloud Service'), (b'CO', 'Community'), (b'DD', 'Direct Download'), (b'GA', 'Game'), (b'PTC', 'Paid-To-Click'), (b'P2P', 'Peer to peer'), (b'SN', 'Social network'), (b'ST', 'Streaming'), (b'TR', 'Tracker')]),
        ),
    ]
