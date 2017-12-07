# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('name', models.CharField(verbose_name='书籍名称', max_length=50)),
                ('desc', models.CharField(verbose_name='书籍简介', max_length=200)),
                ('price', models.DecimalField(verbose_name='书籍价格', max_digits=10, decimal_places=2)),
                ('detail', models.CharField(verbose_name='书籍详情', max_length=500)),
                ('unite', models.CharField(verbose_name='书籍单位', max_length=5)),
                ('type_id', models.SmallIntegerField(default=1, verbose_name='商品种类', choices=[(1, 'python'), (2, 'Javascript'), (3, '数据结构与算法'), (4, '机器学习'), (5, '操作系统'), (6, '数据库')])),
                ('status', models.SmallIntegerField(default=1, verbose_name='商品状态', choices=[(0, '下线'), (1, '上线')])),
            ],
            options={
                'db_table': 's_books',
            },
        ),
    ]
