# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('usersysterm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 1, 3, 34, 45, 614685)),
        ),
        migrations.AlterField(
            model_name='user',
            name='password_hash',
            field=models.CharField(max_length=200),
        ),
    ]
