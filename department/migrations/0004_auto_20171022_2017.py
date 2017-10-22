# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-22 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0003_auto_20171022_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='hostel.Block'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='department.Department'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='floor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='hostel.Floor'),
        ),
    ]