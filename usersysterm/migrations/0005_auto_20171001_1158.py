# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('usersysterm', '0004_auto_20171001_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userextend',
            old_name='user',
            new_name='userlink',
        ),
        migrations.AlterField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 1, 3, 58, 5, 945189)),
        ),
    ]
