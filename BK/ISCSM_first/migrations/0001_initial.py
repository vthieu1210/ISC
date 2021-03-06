# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-03 02:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Firewall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Allow', models.BooleanField(default=True)),
                ('Way', models.CharField(choices=[('in', 'IN'), ('out', 'OUT')], default='in', max_length=5)),
                ('Port', models.CharField(blank=True, max_length=5, null=True)),
                ('SourceIP', models.GenericIPAddressField(blank=True, null=True, protocol='IPv4')),
                ('DestinationIP', models.GenericIPAddressField(blank=True, null=True, protocol='IPv4')),
                ('Description', models.TextField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LocationName', models.CharField(blank=True, max_length=50, null=True)),
                ('Rack', models.CharField(blank=True, max_length=50, null=True)),
                ('Unit', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ServerName', models.CharField(blank=True, max_length=50, null=True)),
                ('OS', models.CharField(choices=[('wds', 'Windows'), ('lns', 'Linux')], default='lns', max_length=3)),
                ('OS_Name', models.CharField(blank=True, max_length=50, null=True)),
                ('IP', models.GenericIPAddressField(protocol='IPv4', unique=True)),
                ('Function', models.CharField(blank=True, max_length=50, null=True)),
                ('Description', models.TextField(blank=True, max_length=50, null=True)),
                ('ServerType', models.CharField(blank=True, max_length=50, null=True)),
                ('CPU', models.CharField(blank=True, max_length=50, null=True)),
                ('RAM', models.CharField(blank=True, max_length=50, null=True)),
                ('HDD', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ServiceName', models.CharField(blank=True, max_length=50, null=True)),
                ('ServiceType', models.CharField(choices=[('win', 'win'), ('web', 'web'), ('db', 'db')], default='win', max_length=5)),
                ('URL', models.URLField(blank=True, null=True)),
                ('RunningAs', models.CharField(blank=True, max_length=50, null=True)),
                ('Description', models.TextField(blank=True, max_length=300, null=True)),
                ('URLWEBS', models.URLField(blank=True, null=True)),
                ('Header', models.TextField(blank=True, max_length=800, null=True)),
                ('Body', models.TextField(blank=True, max_length=1000, null=True)),
                ('Server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISCSM.ServerInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SwitchIP', models.GenericIPAddressField(blank=True, null=True, protocol='IPv4')),
                ('SwitchType', models.CharField(choices=[('cso', 'Cisco'), ('dtk', 'DrayTek')], default='dtk', max_length=5)),
                ('SwitchPort', models.CharField(blank=True, max_length=10, null=True)),
                ('SwitchLocation', models.CharField(blank=True, max_length=10, null=True)),
                ('Server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISCSM.ServerInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ZoneName', models.CharField(max_length=50)),
                ('Description', models.TextField(blank=True, max_length=50, null=True)),
                ('Network', models.GenericIPAddressField(blank=True, default=None, null=True, protocol='IPv4', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='serverinfo',
            name='ZoneName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISCSM.Zone'),
        ),
        migrations.AddField(
            model_name='location',
            name='Server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISCSM.ServerInfo'),
        ),
        migrations.AddField(
            model_name='firewall',
            name='Server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISCSM.ServerInfo'),
        ),
    ]
