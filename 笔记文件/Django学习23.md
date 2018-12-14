# html表单提交评论

> 登录成功后留在当前页面而不是跳转首页

`mysite/views.py`
```python
from django.urls import reverse # 反向通过别名得到网址

def login(request): # 登录
    username = request.POST.get('username','') # 传进来POST是字典形式 如果获取不到username 设置为''(空)
    password = request.POST.get('password','')
    user = auth.authenticate(request, username=username,password=password) # 验证数据库中是否有对应账号密码
    referer =  request.META.get('HTTP_REFERER', reverse('home')) # 获取是从哪个网址跳转过来的 如果获取不到 那么返回首页(通过别名反向得到链接)
    if user is not None: 
        auth.login(request, user) # 存在 登录,有人说login这个会自动提醒如果不正确
        return redirect(referer) # 跳转到之前访问的那一页
    else:
        return render(request, 'error.html',{'message':'用户名或密码不正确'}) # 验证失败 跳转到错误页面

```
> 提交评论 

通过form标签 上传信息
`blog_deatil.html`
```html
<div class="comment-area">
    <h3 class="comment-area-title">提交评论</h3>
    {% if user.is_authenticated %}
        {{ user.username }} 欢迎评论~~
        <form action="{% url 'update_comment' %}" method="POST"> <!--发布评论  发送给提交页面-->
            {% csrf_token %} 
            <textarea name="text" id="comment_text" > 

            </textarea><!--评论框 允许输入换行-->
            <input type="hidden" name= "object_id" value="{{ blog.pk }}"> <!--博客id hidden 表示隐藏-->
            <input type="hidden" name="content_type" value="blog"> <!--文章类型是博客-->
            <input type="submit" value="评论">
        </form>
    {% else %}
        未登录,登录之后方可评论
        <form action="{% url 'login' %}" method="POST"> <!--弹出文本框-->
            {% csrf_token %}   <!--csrf令牌 安全性-->
            <span>用户名: </span>
            <input type="text" name="username"> <!--账号 text是明文-->
            <span>密码: </span>
            <input type="password" name="password"> <!--密码 password 是密文-->
            <input type="submit" value="登录"> <!--submit是按钮  发生数据至上面action的网址-->
        </form>
    {% endif %}
</div>
```
`comment/urls.py` 设置评论的提交页面
```python
from django.urls import path
from . import  views

urlpatterns = [
    path('update_comment',views.update_comment,name='update_comment'), # 提交评论
]
```
`mysite/urls.py` 
```python

from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from . import  views

urlpatterns = [
    path('',views.home,name='home'),
    path('admin/', admin.site.urls),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('blog/',include('blog.urls')),
    path('login/',views.login, name='login'), # 登录界面
    path('comment/',include('comment.urls')), # 总路由包含分路由

]

urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
```
`comment/views.py`
```python
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse # 反向通过别名得到网址
from .models import Comment

def update_comment(request): # 提交评论
    user = request.user
    text = request.POST.get('text','') # 评论内容 获取不到为空
    if text == '':

    content_type = request.POST.get('content_type','') # 文章类型
    object_id = int(request.POST.get('object_id','')) #  文章id ,因为get到的是字符串类型 转换为int
    model_class = ContentType.objects.get(model=content_type).model_class() # 得到该文章类型的具体模型 比如这里model_class 可能为Blog
    model_obj = model_class.objects.get(pk=object_id)   # 找到具体哪一篇文章

    comment = Comment() # 实例化一条评论
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    referer =  request.META.get('HTTP_REFERER', reverse('home')) # 获取是从哪个网址跳转过来的 如果获取不到 那么返回首页(通过别名反向得到链接)
    return redirect(referer) 

```

> 显示评论列表
`blog/views.py`  传入评论给模板标签
```python
def blog_detail(request,blog_pk):
    
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog) 
    blog_content_type = ContentType.objects.get_for_model(blog) # 获取与Blog相关联的cotenttype
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk) # 获取对应该博客的评论

    context = {}    
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() # 获取上一篇博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 获取下一篇博客 
    context['blog'] = blog
    context['comments'] = comments
    response = render( request,'blog/blog_detail.html',context) # 响应
    response.set_cookie(read_cookie_key,'true' ) # 键值  权值   max_age有效期持续时间   expires 有效期到多久为止,
    #有了expires 则 max_age 无效 如果两个都不设置  那么打开浏览器时一直有效 关闭浏览器失效 
    return response

```
`blog_detail.html`  逐条显示
```html
<div class="comment-area">
    <h3 class="comment-area-title">评论列表</h3>
    {% for comment in comments %}
        <div>
            {{ comment.user.username }}
            ({{ comment.comment_time|date:"Y-m-d H:n:s" }}):
            {{ comment.text }}
        </div>
    {% empty %}
        暂无评论
    {% endfor %}
</div>
```
`comment/views.py` 判断数据是否合法并保存数据
```python
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse # 反向通过别名得到网址
from .models import Comment

def update_comment(request): # 提交评论
    referer =  request.META.get('HTTP_REFERER', reverse('home')) # 获取是从哪个网址跳转过来的 如果获取不到 那么返回首页(通过别名反向得到链接)
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

    return redirect(referer) 
```
`error.html`
```html
{% extends 'base.html' %}
{% load staticfiles %}

{% block title %}
        我的网站|错误
{% endblock %}

{% block nav_home_active %}
    active
{%endblock%}


{% block content %}
    {{ message }},<a href="{{ redirect_to }}">返回</a>
{% endblock %}
```

> 页面显示优化
`blog_detail.html`
