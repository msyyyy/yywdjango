> 1. 要登陆网站先配置地址

总urls 
```python
from django.contrib import admin
from django.urls import include,path # include 是用来包含分urls的
from blog.views import blog_list 

urlpatterns = [
    path('',blog_list,name='home'), #打开首页我们得到blog_list，别名为home
    path('admin/', admin.site.urls),
    path('blog/',include('blog.urls')),#分urls

]
```
> 2. 配置views文件 你打开网站后看到什么

```python
from django.shortcuts import render_to_response,get_object_or_404
from .models import Blog

def blog_list(request):#定义blog_list方法
    context = {} #前后端分离 ,blog_list前端文件在blog_list.html影响文字效果
    context['blogs'] = Blog.objects.all()
    return render_to_response('blog_list.html',context)

def blog_detail(request,blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog,pk=blog_pk)
    return render_to_response('blog_detail.html',context)
```
> 3. blog_list.html文件
```python
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>我的网站</title>
</head>
    <div>
        <h3>个人博客网站</h3>
    </div>
<body>
    {% for blog in blogs %}
        <a href="{% url 'blog_detail' blog.pk%}">#<a>代表超链接
            <h3> {{ blog.title }}</h3>
        </a>
        <p>{{ blog.content }}</p>
     {% endfor %}
</body>
</html>
```
> 统计博客数

在blog_list.html文件

{{ blogs|length }}

> 如果博客数为空增加提示文本

blog_list.html
```html
    {% for blog in blogs %}
        <a href="{% url 'blog_detail' blog.pk %}">
            <h3> {{ blog.title }}</h3>
        </a>
        <p>{{ blog.content }}</p>
    {% empty %}
        <p>-- 暂无博客，敬请期待--</p>
    {% endfor %}
```

> 限制主业内容的显示字数
```html
<p>{{ blog.content|truncatechars:30}}</p> 显示30个字符
<p>{{ blog.content|truncatewords:30}}</p> 显示30个单词
```

> 增加了随笔分类的链接和随笔的urls

**1.对urlds的增加**
```python
from django.urls import path
from . import  views

urlpatterns = [
    #http://localhost:8000/blog/<int>
    path('<int:blog_pk>',views.blog_detail,name="blog_detail"),
    path('type/<int:blog_type_pk>',views.blogs_with_type,name="blogs_with_type"),
    #新增 http://localhost:8000/blog/type/ 的网址
]
```
**2.现在有网址但相应views还为修改**
```python
def blogs_with_type(request,blog_type_pk):
    context= {}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk) 
    context['blogs'] =Blog.objects.filter(blog_type=blog_type)#显示所有该文章分类的文章
    context['blog_type'] = blog_type
    return render_to_response('blogs_with_type.html',context)
```
**3.新增blogs_with_type.html**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>{{ blog_type.type_name }}</title>
</head>
    
<body>
    <div>
        <a href={% url 'home' %}>
            <h3>个人博客网站</h3>
        </a>  
    </div>
    <hr>
    <h3> {{ blog_type.type_name }} </h3>
    {% for blog in blogs %}
        <a href="{% url 'blog_detail' blog.pk %}">
            <h3> {{ blog.title }}</h3>
        </a>
        <p>{{ blog.content|truncatechars:30}}</p>
    {% empty %}
        <p>-- 暂无博客，敬请期待--</p>
    {% endfor %}
     <p>一共有{{ blogs|length }}篇博客</p>
</body>
</html>
```
> html 

```html
{#  注释  #}
常见过滤器
日期 date
字数截取 truncatechars   truncatewords
        truncatechars_html 忽视html
是否信任html   safe
长度   length

```
