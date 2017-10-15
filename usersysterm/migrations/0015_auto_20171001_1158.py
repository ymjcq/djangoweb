# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('usersysterm', '0014_auto_20171001_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextend',
            name='friendship',
            field=models.ManyToManyField(to='usersysterm.UserExtend', through='usersysterm.Follow'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 1, 3, 58, 11, 804391)),
        ),
    ]
