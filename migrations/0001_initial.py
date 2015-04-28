# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('URLhash', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('jumps', models.PositiveSmallIntegerField(default=1)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('counter', models.PositiveSmallIntegerField()),
                ('active', models.BooleanField(default=False)),
                ('chain', models.ForeignKey(to='inviMarket.Chain')),
                ('nextlink', models.ForeignKey(to='inviMarket.Link', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.PositiveSmallIntegerField(default=0)),
                ('url', models.URLField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('number', models.PositiveSmallIntegerField(default=0)),
                ('to_donate', models.PositiveSmallIntegerField(default=0)),
                ('referral', models.URLField(blank=True)),
                ('weight', models.PositiveSmallIntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.PositiveSmallIntegerField(default=0)),
                ('trades', models.PositiveIntegerField(default=0)),
                ('donations', models.PositiveIntegerField(default=0)),
                ('lang', models.CharField(blank=True, max_length=5, choices=[(b'es_ES', b'Espa\xc3\xb1ol'), (b'en_UK', b'English')])),
                ('activation_key', models.CharField(max_length=40)),
                ('key_expires', models.DateTimeField(auto_now_add=True)),
                ('partners', models.ManyToManyField(related_name=b'partners', to=settings.AUTH_USER_MODEL, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('traded', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteEdition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('url', models.URLField()),
                ('description_en', models.TextField(max_length=400, blank=True)),
                ('source_en', models.URLField(blank=True)),
                ('description_es', models.TextField(max_length=400, blank=True)),
                ('source_es', models.URLField(blank=True)),
                ('webType', models.CharField(max_length=3, choices=[(b'FO', b'Forum'), (b'TR', b'Tracker'), (b'DD', b'Direct Download'), (b'ST', b'Streaming'), (b'CS', b'Cloud Service'), (b'PT', b'Paid-To-Click')])),
                ('category', models.CharField(max_length=3, choices=[(b'GEN', b'Generic'), (b'MMD', b'Multimedia'), (b'COM', b'Commerce'), (b'RE', b'Referral')])),
                ('active', models.BooleanField(default=True)),
                ('protected', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now=True)),
                ('comments', models.TextField(max_length=200, blank=True)),
                ('accepted', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('offer', models.ManyToManyField(to='inviMarket.Offer')),
                ('proposer', models.ForeignKey(related_name=b'trade_proposal', to=settings.AUTH_USER_MODEL)),
                ('receptor', models.ForeignKey(related_name=b'trade_request', to=settings.AUTH_USER_MODEL)),
                ('request', models.ManyToManyField(to='inviMarket.Request')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('url', models.URLField()),
                ('refvalidator', models.CharField(max_length=200, blank=True)),
                ('description_en', models.TextField()),
                ('source_en', models.URLField(blank=True)),
                ('description_es', models.TextField()),
                ('source_es', models.URLField(blank=True)),
                ('webType', models.CharField(max_length=3, choices=[(b'FO', b'Forum'), (b'TR', b'Tracker'), (b'DD', b'Direct Download'), (b'ST', b'Streaming'), (b'CS', b'Cloud Service'), (b'PT', b'Paid-To-Click')])),
                ('category', models.CharField(max_length=3, choices=[(b'GEN', b'Generic'), (b'MMD', b'Multimedia'), (b'COM', b'Commerce'), (b'RE', b'Referral')])),
                ('popularity', models.PositiveSmallIntegerField(default=0)),
                ('requests', models.PositiveIntegerField(default=0)),
                ('offers', models.PositiveIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('protected', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='request',
            name='website',
            field=models.ForeignKey(to='inviMarket.Website'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offer',
            name='website',
            field=models.ForeignKey(to='inviMarket.Website'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='offer',
            field=models.ForeignKey(to='inviMarket.Offer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chain',
            name='website',
            field=models.ForeignKey(to='inviMarket.Website'),
            preserve_default=True,
        ),
    ]
