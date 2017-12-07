from django.db import models
from db.base_model import BaseModel
from hashlib import sha1
# Create your models here.


def get_hash(str):
    sh = sha1()
    sh.update(str.encode('utf8'))
    return sh.hexdigest()


class PassportManager(models.Manager):

    def add_one_passport(self, username, password, email):
        # 添加一个账户信息
        passport = self.create(username=username, password=get_hash(password), email=email)
        return passport

    def get_one_passport(self, username, password):
        # 根据用户名密码查找用户的信息
        try:
            passport = self.get(username=username, password=get_hash(password))
        except self.model.DoesNotExist:
            # 账户不存在
            passport = None
        return passport

    def get_only_name(self,username):
        # 只获得用户名
        try:
            passport = self.get(username=username)
        except self.model.DoesNotExist:
            # 账户不存在
            passport = None
        return passport


class Passport(BaseModel):
    # 用户系统
    # 字段名

    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    is_active = models.BooleanField(default=False, verbose_name='激活')

    # 用户表的管理器
    objects = PassportManager()

    class Meta:
        db_table = 's_user_account'
