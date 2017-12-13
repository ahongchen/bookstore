from django.conf.urls import url
from .views import register, register_handle, login, login_check, logout, user, register_done, address, order, verifycode

urlpatterns = [
    url(r'^register/', register, name='register'),
    url(r'^register_handle/', register_handle, name='register_handle'),
    url(r'^register_done/', register_done, name='register_done'),
    url(r'^login/', login, name='login'),
    url(r'^login_check/', login_check, name='login_check'),
    url(r'^logout/', logout, name='logout'),
    url(r'^user_center/', user, name='user'),
    url(r'^address/', address, name='address'),
    url(r'^order/', order, name='order'),
    url(r'^verifycode/', verifycode, name='verifycode'),
]
