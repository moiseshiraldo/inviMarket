# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inviMarket', '0005_profile_notify'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comments', models.TextField(max_length=400, blank=True)),
                ('trade', models.ForeignKey(to='inviMarket.Trade')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='trade',
            name='completed',
        ),
        migrations.AlterField(
            model_name='profile',
            name='lang',
            field=models.CharField(blank=True, max_length=5, choices=[(b'es-ES', b'Espa\xc3\xb1ol'), (b'en-UK', b'English')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trade',
            name='comments',
            field=models.TextField(max_length=400, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='website',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'static/sites'),
            preserve_default=True,
        ),
    ]
