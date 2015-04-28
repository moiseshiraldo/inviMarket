# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0003_website_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'inviMarket/static/images'),
            preserve_default=True,
        ),
    ]
