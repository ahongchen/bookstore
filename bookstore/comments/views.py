from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from comments.models import Comments
from django.http import JsonResponse
import json
# Create your views here.


@csrf_exempt
def comment(request,books_id):
    if request.method == 'GET':
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