from django.db import models
from db.base_model import BaseModel
from .enums import *
from tinymce.models import HTMLField
# Create your models here.


# 抽取一些基本功能作为基类
class BookManager(models.Manager):
    # 根据商品类型id查询商品信息
    def get_books_by_type(self, type_id, limit=None, sort='default'):
        if sort == 'new':
            order_by = ('-create_time',)
        elif sort == 'hot':
            order_by = ('-sales',)
        elif sort == 'price':
            order_by = ('price',)
        else:
            order_by = ('-pk',)  # 按照primary_key降序排列
        # 查询数据
        books_li = self.filter(type_id=type_id).order_by(*order_by)
        # 查询结果集的限制
        if limit:
            books_li = books_li[:limit]
        return books_li

    def get_books_by_id(self, books_id):
        # 根据书的id获取信息
        try:
            books = self.get(id=books_id)
        except self.model.DoesNotExist:
            books = None
        return books


class Books(BaseModel):
    book_type_choices = ((k, v) for k, v in BOOK_TYPE.items())
    status_choices = ((k, v) for k, v in STATUS_CHOICE.items())
    name = models.CharField(max_length=50, verbose_name='书籍名称')
    desc = models.CharField(max_length=200, verbose_name='书籍简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='书籍价格')
    detail = models.CharField(max_length=500, verbose_name='书籍详情')
    unite = models.CharField(max_length=5, verbose_name='书籍单位')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    type_id = models.SmallIntegerField(default=PYTHON, choices=book_type_choices, verbose_name='商品种类')
    status = models.SmallIntegerField(default=ONLINE, choices=status_choices, verbose_name='商品状态')
    # 使用富文本编辑器
    details = HTMLField(default='')
    image = models.ImageField(default='', upload_to='books', verbose_name='商品图片')
    objects = BookManager()

    class Meta:
        db_table = 's_books'
