# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usersysterm', '0003_auto_20171001_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtend',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('about_me', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='friendship',
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='followed',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='follower_set'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='followed_set'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 1, 3, 41, 32, 400418)),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='userextend',
            name='friendship',
            field=models.ManyToManyField(through='usersysterm.Follow', to='usersysterm.UserExtend'),
        ),
        migrations.AddField(
            model_name='userextend',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
