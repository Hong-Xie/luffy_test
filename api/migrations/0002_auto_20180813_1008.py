# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-13 02:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
                ('type', models.IntegerField(choices=[(1, 'common'), (2, 'VIP'), (3, 'SVIP')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=128)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name_plural': '专题课'},
        ),
        migrations.AlterModelOptions(
            name='coursedetail',
            options={'verbose_name_plural': '课程详细'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name_plural': '讲师'},
        ),
    ]
