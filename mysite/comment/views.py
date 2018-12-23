from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse # 反向通过别名得到网址
from django.http import JsonResponse 
from .models import Comment
from .forms import CommentForm

def update_comment(request): # 提交评论

    referer =  request.META.get('HTTP_REFERER', reverse('home')) # 获取是从哪个网址跳转过来的 如果获取不到 那么返回首页(通过别名反向得到链接)
    comment_form = CommentForm(request.POST,user=request.user) # 实例化 把user传到CommentForm
    data = {}
    if comment_form.is_valid():
        # 检查已通过,保存数据
        comment = Comment() # 实例化一条评论
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        
        # 返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S') # 字符串化时间
        data['text'] = comment.text
    else:
        # return render(request, 'error.html',{'message':comment_form.errors,'redirect_to': referer })
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
