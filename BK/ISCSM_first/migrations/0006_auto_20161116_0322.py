# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 03:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISCSM', '0005_auto_20161011_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverinfo',
            name='CPU',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]