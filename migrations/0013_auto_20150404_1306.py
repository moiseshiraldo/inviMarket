# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import inviMarket.models


class Migration(migrations.Migration):

    dependencies = [
        ('inviMarket', '0012_auto_20150325_2310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('source', models.URLField(blank=True)),
                ('lang', models.CharField(blank=True, max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English')])),
                ('site', models.ForeignKey(to='inviMarket.Website')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='website',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='website',
            name='description_es',
        ),
        migrations.RemoveField(
            model_name='website',
            name='source_en',
        ),
        migrations.RemoveField(
            model_name='website',
            name='source_es',
        ),
        migrations.AddField(
            model_name='siteedition',
            name='lang',
            field=models.CharField(default='en', max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=inviMarket.models.avatar_file_name, validators=[inviMarket.models.validate_image]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='lang',
            field=models.CharField(blank=True, max_length=5, choices=[(b'es', 'Spanish'), (b'en', 'English')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='website',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'sites/'),
            preserve_default=True,
        ),
    ]
