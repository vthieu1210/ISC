# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-31 07:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISCSM', '0009_auto_20170105_0259'),
    ]

    operations = [
        migrations.AddField(
            model_name='firewall',
            name='DateCreate',
            field=models.DateField(blank=True, default=datetime.datetime.today, null=True),
        ),
    ]
