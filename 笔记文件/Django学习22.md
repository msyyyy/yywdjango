# 评论功能设计和用户登录

评论对象  评论内容  评论时间 评论者

> 1. python3 manage.py startapp comment 创建评论app  

> 2. 添加models
```python
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 
from django.contrib.auth.models import User

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING) # models.CASCADE 删除阅读次数会删除博客   DO_NOTHING  删除阅读次数对应博客本身无影响
    object_id = models.PositiveIntegerField()  
    content_object = GenericForeignKey('content_type', 'object_id') # 评论对象

    text = models.TextField() # 评论内容
    comment_time = models.DateTimeField(auto_now_add=True) # 评论时间
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING) # 评论者
```
> 3. 后台显示 admin
```python
from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object','text','comment_time','user')
```
> 4. setting 增加app 然后更新数据库

> 5. 
### 如何判读用户是否登录
user.is_authenticated 登录返回True
`blog/views.py`
```python
def blog_detail(request,blog_pk):
    
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog) 
     
    context = {}    
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() # 获取上一篇博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 获取下一篇博客 
    context['blog'] = blog
    context['user'] = request.user # 返回登录用户
    response = render( request,'blog/blog_detail.html',context) # 响应
    response.set_cookie(read_cookie_key,'true' ) # 键值  权值   max_age有效期持续时间   expires 有效期到多久为止,
    #有了expires 则 max_age 无效 如果两个都不设置  那么打开浏览器时一直有效 关闭浏览器失效 
    return response
```
`blog/blog_detail.html`
```html
 <div class="row">
    <div class="col-xs-10 col-xs-offset-1">
        <div>提交评论区
            {% if user.is_authenticated %}
                已登录
            {% else %}
                未登录
                <form action="{% url 'login' %}" method="POST"> <!--弹出文本框--> 
                    {% csrf_token %}   <!--csrf令牌 安全性-->
                    <input type="text" name="username"> <!--账号 text是明文-->
                    <input type="password" name="password"> <!--密码 password 是密文-->
                    <input type="submit" value="登录"> <!--submit是按钮  发生数据至上面action的网址-->
                </form>
            {% endif %}
        </div>
        <div>评论列表区</div>
    </div>
</div>
```
`mysite/urls.py`
```python
   path('login/',views.login, name='login'), # 登录界面
```
`mysite/views.py`
这边用的都是render而不是render_for_request ,render比较好 
render(request, )
render_for_request( , )
```python
def login(request): # 登录
    username = request.POST.get('username','') # 传进来POST是字典形式 如果获取不到username 设置为''(空)
    password = request.POST.get('password','')
    user = auth.authenticate(request, username=username,password=password) # 验证数据库中是否有对应账号密码
    if user is not None: 
        auth.login(request, user) # 存在 登录,有人说login这个会自动提醒如果不正确
        return redirect('/') # 跳转到首页
    else:
        return render(request, 'error.html',{'message':'用户名或密码不正确'}) # 验证失败 跳转到错误页面,
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
    {{ message }}
{% endblock %}
```