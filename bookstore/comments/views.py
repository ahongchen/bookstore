from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from comments.models import Comments
from django.http import JsonResponse
import json
import redis
# Create your views here.
EXPIRE_TIME = 60 * 10
pool = redis.ConnectionPool(host='localhost', port=6379, db=2)
redis_db = redis.Redis(connection_pool=pool)


@csrf_exempt
def comment(request,books_id):
    book_id = books_id
    if request.method == 'GET':
        c = redis_db.get('comment_%s'%book_id)
        try:
            c = c.decode('utf-8')
        except:
            pass
        print('c:', c)

        if c:
            return JsonResponse({
                'code': 200,
                'data': json.loads(c),

            })
        else:
            comments = Comments.objects.get_comments(book_id=books_id)
            data = []
            for c in comments:
                data.append({
                    'user_id': c.user_id,
                    'content': c.content,
                })
            res = {
                'code': 200,
                'data': data,
            }
            try:
                redis_db.setex('comment_%s'%book_id, json.dumps(data), EXPIRE_TIME)
            except Exception as e:
                print('e:',e)
            return JsonResponse(res)

    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        content = data.get('content')
        book_id = data.get('book_id')
        user_id = request.session.get('passport_id')
        print(data)
        c = Comments(content=content, book_id=book_id, passport_id=user_id)
        c.save()
        return JsonResponse({
            'code': 200,
            'msg': '评论成功',
        })