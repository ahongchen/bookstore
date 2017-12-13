from django.db import models
from db.base_model import BaseModel
from users.models import Passport
from books.models import Books
# Create your models here.


class CommentsManager(models.Manager):
    def get_comments(self, book_id):
        try:
            comments = self.get(book=book_id)
        except self.model.DoesNotExist:
            comments = None
        return comments


class Comments(BaseModel):
    # 评论的字段设计
    show = models.BooleanField(default=True, verbose_name='显示评论')
    content = models.CharField(max_length=1000, verbose_name='评论内容')
    passport = models.ForeignKey('users.Passport', verbose_name='用户ID')
    book = models.ForeignKey('books.Books', verbose_name='书籍ID')

    objects = CommentsManager()

    class Meta:
        db_table = 's_comments'
