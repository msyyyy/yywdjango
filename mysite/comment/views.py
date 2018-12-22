from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse # 反向通过别名得到网址
from .models import Comment
from .forms import CommentForm

def update_comment(request): # 提交评论

    referer =  request.META.get('HTTP_REFERER', reverse('home')) # 获取是从哪个网址跳转过来的 如果获取不到 那么返回首页(通过别名反向得到链接)
    comment_form = CommentForm(request.POST,user=request.user) # 实例化 把user传到CommentForm
    
    if comment_form.is_valid():
        # 检查已通过,保存数据
        comment = Comment() # 实例化一条评论
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        return redirect(referer)
    else:
        return render(request, 'error.html',{'message':comment_form.errors,'redirect_to': referer })