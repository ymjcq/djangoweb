# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('usersysterm', '0005_auto_20171001_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followed',
            field=models.ForeignKey(to='usersysterm.UserExtend', related_name='follower_set'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(to='usersysterm.UserExtend', related_name='followed_set'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 1, 3, 44, 9, 49130)),
        ),
    ]
