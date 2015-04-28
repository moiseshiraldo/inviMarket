# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inviMarket', '0020_auto_20150422_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_address', models.CharField(max_length=320)),
                ('subject', models.TextField()),
                ('text', models.TextField()),
                ('complaint', models.ForeignKey(to='inviMarket.Complaint')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='complaint',
            name='accepted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complaint',
            name='auto',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='complaint',
            name='receptor',
            field=models.ForeignKey(related_name='received_complaints', default='', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
