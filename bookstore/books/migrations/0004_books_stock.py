# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_books_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='stock',
            field=models.IntegerField(verbose_name='商品库存', default=1),
        ),
    ]
