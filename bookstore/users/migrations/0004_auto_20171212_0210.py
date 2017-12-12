# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='passport',
            options={'verbose_name_plural': '基本信息', 'verbose_name': '基本信息'},
        ),
    ]
