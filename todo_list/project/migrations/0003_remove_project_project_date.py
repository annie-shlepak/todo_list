# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 21:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_date',
        ),
    ]