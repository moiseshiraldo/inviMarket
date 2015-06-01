# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import inviMarket.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_hash', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=20, blank=True)),
                ('jumps', models.PositiveSmallIntegerField(default=1)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auto', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('comments', models.TextField(max_length=400, blank=True)),
                ('receptor', models.ForeignKey(related_name='received_complaints', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('source', models.URLField(blank=True)),
                ('lang', models.CharField(blank=True, max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English')])),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_address', models.CharField(max_length=320)),
                ('subject', models.TextField()),
                ('text', models.TextField()),
                ('complaint', models.ForeignKey(to='inviMarket.Complaint')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('counter', models.PositiveSmallIntegerField()),
                ('active', models.BooleanField(default=False)),
                ('last_link', models.BooleanField(default=False)),
                ('chain', models.ForeignKey(to='inviMarket.Chain')),
                ('next_link', models.ForeignKey(related_name='previous_link', blank=True, to='inviMarket.Link', null=True)),
                ('source_link', models.ForeignKey(related_name='children_links', blank=True, to='inviMarket.Link', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.PositiveSmallIntegerField(default=0)),
                ('url', models.URLField()),
                ('date', models.DateField(auto_now=True)),
                ('sender', models.ForeignKey(related_name='sent_notification', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
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
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=inviMarket.models.avatar_file_name, validators=[inviMarket.models.validate_image])),
                ('rating', models.PositiveSmallIntegerField(default=35)),
                ('trades', models.PositiveIntegerField(default=0)),
                ('donations', models.PositiveIntegerField(default=0)),
                ('lang', models.CharField(blank=True, max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English')])),
                ('activation_key', models.CharField(max_length=40)),
                ('key_expires', models.DateTimeField(null=True, blank=True)),
                ('last_visit', models.DateTimeField(null=True, blank=True)),
                ('notify', models.BooleanField(default=True)),
                ('locked', models.BooleanField(default=False)),
                ('partners', models.ManyToManyField(related_name='partners', to=settings.AUTH_USER_MODEL, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('traded', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SiteEdition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('name', models.CharField(max_length=20)),
                ('url', models.URLField()),
                ('refvalidator', models.CharField(max_length=200, blank=True)),
                ('email_domain', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField(max_length=5000, blank=True)),
                ('source', models.URLField(null=True, blank=True)),
                ('lang', models.CharField(max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English'), (b'multi', 'Multi-language')])),
                ('webType', models.CharField(max_length=3, choices=[(b'APP', 'Application'), (b'CS', 'Cloud Service'), (b'DD', 'Direct Download'), (b'FO', 'Forum'), (b'PTC', 'Paid-To-Click'), (b'P2P', 'Peer to peer'), (b'ST', 'Streaming'), (b'TR', 'Tracker')])),
                ('category', models.CharField(max_length=3, choices=[(b'EC', 'E-commerce'), (b'GEN', 'Generic'), (b'MMD', 'Multimedia'), (b'RE', 'Referral'), (b'TEL', 'Telecommunications')])),
                ('active', models.BooleanField(default=True)),
                ('comments', models.TextField(max_length=400, blank=True)),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('donation', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('comments', models.TextField(max_length=400, blank=True)),
                ('accepted', models.BooleanField(default=False)),
                ('offers', models.ManyToManyField(to='inviMarket.Offer')),
                ('proposer', models.ForeignKey(related_name='proposed_trades', to=settings.AUTH_USER_MODEL)),
                ('receptor', models.ForeignKey(related_name='received_trades', to=settings.AUTH_USER_MODEL)),
                ('requests', models.ManyToManyField(to='inviMarket.Request')),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20, db_index=True)),
                ('url', models.URLField()),
                ('logo', models.ImageField(null=True, upload_to=b'sites/', blank=True)),
                ('refvalidator', models.CharField(max_length=200, blank=True)),
                ('email_domain', models.CharField(db_index=True, max_length=200, blank=True)),
                ('lang', models.CharField(blank=True, max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English'), (b'multi', 'Multi-language')])),
                ('webType', models.CharField(max_length=3, choices=[(b'APP', 'Application'), (b'CS', 'Cloud Service'), (b'DD', 'Direct Download'), (b'FO', 'Forum'), (b'PTC', 'Paid-To-Click'), (b'P2P', 'Peer to peer'), (b'ST', 'Streaming'), (b'TR', 'Tracker')])),
                ('category', models.CharField(max_length=3, choices=[(b'EC', 'E-commerce'), (b'GEN', 'Generic'), (b'MMD', 'Multimedia'), (b'RE', 'Referral'), (b'TEL', 'Telecommunications')])),
                ('popularity', models.PositiveSmallIntegerField(default=0)),
                ('requests', models.PositiveIntegerField(default=0)),
                ('offers', models.PositiveIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('protected', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='siteedition',
            name='site',
            field=models.ForeignKey(blank=True, to='inviMarket.Website', null=True),
        ),
        migrations.AddField(
            model_name='siteedition',
            name='user',
            field=models.ForeignKey(related_name='editions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='request',
            name='website',
            field=models.ForeignKey(to='inviMarket.Website'),
        ),
        migrations.AddField(
            model_name='offer',
            name='website',
            field=models.ForeignKey(to='inviMarket.Website'),
        ),
        migrations.AddField(
            model_name='description',
            name='site',
            field=models.ForeignKey(to='inviMarket.Website'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='trade',
            field=models.ForeignKey(to='inviMarket.Trade'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chain',
            name='website',
            field=models.ForeignKey(to='inviMarket.Website'),
        ),
    ]
