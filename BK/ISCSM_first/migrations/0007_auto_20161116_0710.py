# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISCSM', '0006_auto_20161116_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverinfo',
            name='Description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='serverinfo',
            name='HDD',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='serverinfo',
            name='RAM',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
