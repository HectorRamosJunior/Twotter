# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 01:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twotter', '0006_auto_20160428_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twoot',
            name='twotter_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='twoots', to='twotter.TwotterProfile'),
        ),
    ]
