from django.conf.urls import url
from .views import comment


urlpatterns = [
    url(r'^user_comments/(?P<books_id>\d+)/', comment, name='comment'),
]
