from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from users.models import Passport,Address
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from utils.decorators import login_required
# Create your views here.


def register(request):
    return render(request, 'users/register.html')


# 由前端传回来的表单数据
@csrf_exempt
def register_handle(request):
    # 接收数据
    data = json.loads(request.body.decode('utf-8'))

    username = data.get('username', '')
    # 进行数据校验
    if not all([username]):
        # 有空的数据
        return JsonResponse({'code': 500})
    # 判断邮箱是否合法 TODO
    p = Passport.objects.get_only_name(username)
    if not p:
        # 返回登录页
        # return redirect(reverse('user:login'))
        return JsonResponse({'res': 1})
    return JsonResponse({'res': 500})


@csrf_exempt
def register_done(request):
    # 接收数据
    data = json.loads(request.body.decode('utf-8'))

    username = data.get('username', '')
    password = data.get('password', '')
    email = data.get('email', '')
    # 向系统中添加账户
    Passport.objects.add_one_passport(username=username, password=password, email=email)
    # 返回登录页
    # return redirect(reverse('user:login'))
    return JsonResponse({'res': 1})


def login(request):
    # 判断cookie中是否有username
    if 'username' in request.COOKIES:
        context = {
            'username': request.COOKIES['username'],
            'checked': 'checked'
        }
    else:
        context = {
            'username': '',
            'password': '',
        }
    return render(request, 'users/login.html', context)


@csrf_exempt
def login_check(request):
    # username = request.POST.get('username')
    # password = request.POST.get('pwd')
    # remember = request.POST.get('remember')
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username', '')
    password = data.get('password', '')
    remember = data.get('remember', '')
    if not all([username, password]):
        return JsonResponse({'res': 499})
    # 查找账户信息
    passport = Passport.objects.get_one_passport(username, password)
    # 验证通过
    if passport:
        next_url = request.session.get('url_path', reverse('books:index'))
        jres = JsonResponse({'res': 1, 'next_url': next_url})
        # 是否记住用户名
        if remember:
            jres.set_cookie('username', username, max_age=7*24*3600)
        else:
            jres.delete_cookie('username')
        # 记住登录状态
        request.session['islogin'] = True
        request.session['username'] = username
        request.session['passport_id'] = passport.id
        # 返回json串
        return jres
    else:
        # 用户或密码错误
        p = Passport.objects.get_only_name(username)
        if not p:
            # 用户名不存在
            return JsonResponse({'res': 500})
        # 密码错误
        return JsonResponse({'res': 501})


def logout(request):
    # 清空session信息
    request.session.flush()
    # 重定向到首页
    return redirect(reverse('books:index'))


@login_required
def user(request):
    '''用户中心-信息页'''
    passport_id = request.session.get('passport_id')
    # 获取用户的基本信息
    addr = Address.objects.get_default_address(passport_id=passport_id)

    books_li = []

    context = {
        'addr': addr,
        'page': 'user',
        'books_li': books_li
    }

    return render(request, 'users/user_center_info.html', context)
