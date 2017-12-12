# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_books_stock'),
        ('users', '0003_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('count', models.IntegerField(verbose_name='商品数量', default=1)),
                ('price', models.DecimalField(verbose_name='商品价格', decimal_places=2, max_digits=10)),
                ('books', models.ForeignKey(to='books.Books', verbose_name='订单商品')),
            ],
            options={
                'db_table': 's_order_books',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('order_id', models.CharField(verbose_name='订单编号', serialize=False, max_length=64, primary_key=True)),
                ('total_count', models.IntegerField(verbose_name='商品总数', default=1)),
                ('total_price', models.DecimalField(verbose_name='商品总价', decimal_places=2, max_digits=10)),
                ('transit_price', models.DecimalField(verbose_name='订单运费', decimal_places=2, max_digits=10)),
                ('pay_method', models.SmallIntegerField(verbose_name='支付方式', choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], default=1)),
                ('status', models.SmallIntegerField(verbose_name='订单状态', choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], default=1)),
                ('trade_id', models.CharField(blank=True, verbose_name='支付编号', max_length=100, null=True, unique=True)),
                ('addr', models.ForeignKey(to='users.Address', verbose_name='收货地址')),
                ('passport', models.ForeignKey(to='users.Passport', verbose_name='下单账户')),
            ],
            options={
                'db_table': 's_order_info',
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(to='order.OrderInfo', verbose_name='所属订单'),
        ),
    ]
