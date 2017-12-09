from django.conf.urls import url
from .views import cart_add, cart_count, cart_show, cart_del, cart_update


urlpatterns = [
    url(r'^add/', cart_add, name='add'),
    url(r'^count/', cart_count, name='count'),  # 获取购物车种商品的数量
    url(r'^$', cart_show, name='cart_show'),  # 显示用户的购物车页面
    url(r'^del/', cart_del, name='cart_del'),  # 购物车商品记录删除
    url(r'^update/', cart_update, name='cart_update'),  # 更新购物车商品数目
]
