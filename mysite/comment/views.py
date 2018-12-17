from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse # 反向通过别名得到网址
from .models import Comment

def update_comment(request): # 提交评论
    '''referer =  request.META.get('HTTP_REFERER', reverse('home')) # 获取是从哪个网址跳转过来的 如果获取不到 那么返回首页(通过别名反向得到链接)
    user = request.user
    # 数据检查
    if not user.is_authenticated: # 因为前端页面不是绝对可靠的,所有再次判断
        return render(request, 'error.html',{'message':'用户未登录','redirect_to': referer }) # 用户未登录

    text = request.POST.get('text','').strip() # 评论内容 获取不到为空.strip 会把头的无效空格去掉
    if text == '':
        return render(request, 'error.html',{'message':'评论内容为空','redirect_to': referer }) # 空的无效评论 

    try:
        content_type = request.POST.get('content_type','') # 文章类型
        object_id = int(request.POST.get('object_id','')) #  文章id ,因为get到的是字符串类型 转换为int
        model_class = ContentType.objects.get(model=content_type).model_class() # 得到该文章类型的具体模型 比如这里model_class 可能为Blog
        model_obj = model_class.objects.get(pk=object_id)   # 找到具体哪一篇文章
    except Exception as e:
        return render(request, 'error.html',{'message':'评论对象不存在','redirect_to': referer }) # 如果上面会返回错误信息

    # 检查已通过,保存数据
    comment = Comment() # 实例化一条评论
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()

    return redirect(referer) '''

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