# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('usersysterm', '0015_auto_20171001_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userextend',
            name='friendship',
        ),
        migrations.AddField(
            model_name='userextend',
            name='mingxing',
            field=models.ManyToManyField(through='usersysterm.Follow', related_name='fensi', to='usersysterm.UserExtend'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 1, 3, 15, 54, 760693)),
        ),
    ]
