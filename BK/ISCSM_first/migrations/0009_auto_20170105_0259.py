# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-05 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISCSM', '0008_auto_20161116_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firewall',
            name='Description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='zone',
            name='Description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
