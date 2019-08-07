# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('ip', models.CharField(verbose_name='ip', max_length=255)),
                ('ip_status', models.CharField(verbose_name='ip状态', max_length=255, blank=True, null=True)),
                ('add_time', models.DateTimeField(verbose_name='添加时间', null=True, auto_now_add=True)),
                ('comment', models.CharField(verbose_name='备注', max_length=255, blank=True, null=True)),
            ],
            options={
                'db_table': 'xy_ip',
            },
        ),
    ]
