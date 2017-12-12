from django.shortcuts import render,redirect
from utils.decorators import login_required
from django.core.urlresolvers import reverse
from order.models import OrderGoods, OrderInfo
from books.models import Books
from users.models import Address
from django_redis import get_redis_connection
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .enums import PAY_METHOD_CHOICES, PAY_METHODS_ENUM
import os
import time
from django.db import transaction
# Create your views here.


@login_required
def order_place(request):
    '''显示提交订单页面'''
    # 接收数据
    books_ids = request.POST.getlist('books_ids')
    # 校验数据
    if not all(books_ids):
        return redirect(reverse('cart:show'))
    # 用户收货地址
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)
    # 用户要购买商品的信息
    books_li = []
    # 商品的总数目和总金额
    total_count = 0
    total_price = 0

    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%passport_id

    for id in books_ids:
        # 根据id获取商品的信息
        books = Books.objects.get_books_by_id(books_id=id)
        # 从redis中获取用户要购买的商品的数目
        count = conn.hget(cart_key, id)
        books.count = count
        # 计算商品的小计
        amount = int(count) * books.price
        books.amount = amount
        books_li.append(books)
        # 累计计算商品的总数目和总金额
        total_count += int(count)
        total_price += books.amount
    # 商品运费和实付款
    transit_price = 12
    total_pay = total_price + transit_price
    # 切割
    books_ids = ','.join(books_ids)
    context = {
        'addr': addr,
        'books_li': books_li,
        'total_price': total_price,
        'transit_price': transit_price,
        'total_pay': total_pay,
        'books_ids': books_ids
    }
    return render(request, 'order/place_order.html', context)


@transaction.atomic
def order_commit(request):
    '''生成订单'''
    # 验证用户是否登录
    print('11111111111')
    if not request.session.has_key('islogin'):
        return JsonResponse({'res': 0, 'errmsg': '用户未登陆'})
    # 接收数据
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    books_ids = request.POST.get('books_ids')
    # 进行数据校验
    if not all ([addr_id, pay_method, books_ids]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
    try:
        addr = Address.objects.get(id=addr_id)
    except Exception as e:
        # 地址信息出错
        return JsonResponse({'res': 2, 'errmsg': '地址信息错误'})
    if int(pay_method) not in PAY_METHODS_ENUM.values():
        return  JsonResponse({'res': 3, 'errmsg': '不支持的支付方式'})
    # 订单创建
    # 组织订单信息
    passport_id = request.session.get('passport_id')
    # 订单id: 20171029110830+用户的id
    order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(passport_id)
    # 运费
    transit_price = 10
    # 订单商品总数和总金额
    total_count = 0
    total_price = 0
    # 创建一个保存点
    sid = transaction.savepoint()
    try:
        # 向订单中信息表中添加一条记录
        order = OrderInfo.objects.create(order_id=order_id,
                                         passport_id=passport_id,
                                         addr_id=addr_id,
                                         total_price=total_price,
                                         total_count=total_count,
                                         transit_price=transit_price,
                                         pay_method=pay_method,)
        # 向订单商品表中添加商品的记录
        books_ids =books_ids.split(',')
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%passport_id
        # 遍历获取用户购买的商品信息
        for id in books_ids:
            books = Books.objects.get_books_by_id(books_id=id)
            if books is None:
                # 回滚到上个存档点
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 4, 'errmsg': '商品信息错误'})
            # 获取用户购买的商品数目
            count = conn.hget(cart_key, id)
            # 判断商品的库存
            if int(count) > books.stock:
                # 库存不足,回滚
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 5, 'errmsg': '商品库存不足'})
            # 创建一条订单商品记录
            OrderGoods.objects.create(order_id=order_id,
                                      books_id=id,
                                      count=count,
                                      price=books.price)
            # 增加商品的数量,减少商品库存
            books.sales += int(count)
            books.stock -= int(count)
            books.save()
            # 计算累计商品的总数目和总额
            total_count += int(count)
            transit_price += int(count) * books.price
        # 更新订单的商品总数目和总金额
        order.total_count = total_count
        order.total_price = total_price
        order.save()
    except Exception as e:
        # 操作数据库出错,进行回滚操作
        transaction.savepoint_rollback(sid)
        return JsonResponse({'res': 7, 'errmsg': '服务器错误'})
    # 清除购物车对应记录
    conn.hdel(cart_key, *books_ids)
    # 事务提交
    transaction.savepoint_commit(sid)
    # 返回应答

    return JsonResponse({'res': 6})
