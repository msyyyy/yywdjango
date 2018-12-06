# bootstrap响应式布局
根据屏幕大小自动更改显示效果
> 新增博客分类
`views.py`
```python
from django.shortcuts import render_to_response,get_object_or_404
from .models import Blog,BlogType

def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    context['blog_types'] = BlogType.objects.all()  新放入所有博客分类
    return render_to_response('blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog,pk=blog_pk)
    return render_to_response('blog/blog_detail.html',context)

def blogs_with_type(request,blog_type_pk):
    context= {}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    context['blogs'] =Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html',context)
```


`blog_list.html`
**加了面板效果**
```html
{% extends 'base.html' %}

{# 页面标签 #}
{% block title %} 
    我的网站
{% endblock %}

{% block nav_blog_active %}
    active
{%endblock%}

{# 页面内容 #}
{% block content %}
    <div class="container">
        <div class="row">
            <div class="col-md-8"> 屏幕一行一共12 ，这个每行占了8  下一个占了4
                {% for blog in blogs %}
                    <a href="{% url 'blog_detail' blog.pk %}">
                        <h3> {{ blog.title }}</h3>
                    </a>
                    <p>{{ blog.content|truncatechars:30}}</p>
                {% empty %}
                    <p>-- 暂无博客，敬请期待--</p>
                {% endfor %}
                <p>一共有{{ blogs|length }}篇博客</p>
            </div>
            <div class="col-md-4">
                <div class="panel panel-default">
                    <div class="panel-heading">博客分类</div>
                    <div class="panel-body">
                        <ul style="list-style-type: none;">去掉面板中每一个分类前的小黑点
                            {% for  blog_type in blog_types %}
                                <li>
                                    <a href="{% url 'blogs_with_type' blog_type.pk %}">{{ blog_type.type_name }}</a>
                                    前一个是url中的别名 后一个是每一个博客分类具体的id值
                                </li>
                            {% empty %}
                                <li>暂无分类</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
{% endblock %}

```

> 分别的屏幕设置
`blog_list`

```html
{% block content %}
    <div class="container">
        <div class="row">
            <div class=" col-xs-12 col-sm-8 col-md-9 col-lg-10"> 
                <div class="panel panel-default">
                    <div class="panel-heading">博客列表 (一共有{{ blogs|length }}篇博客)</div>
                    <div class="panel-body">
                        {% for blog in blogs %}
                        <a href="{% url 'blog_detail' blog.pk %}">
                            <h3> {{ blog.title }}</h3>
                        </a>
                        <p>{{ blog.content|truncatechars:30}}</p>
                        {% empty %}
                            <p>-- 暂无博客，敬请期待--</p>
                        {% endfor %}
                    </div>

                </div>
            </div>
            <div class=" hidden-xs col-sm-4 col-md-3 col-lg-2"> 小屏幕隐藏
                <div class="panel panel-default">
                    <div class="panel-heading">博客分类</div>
                    <div class="panel-body">
                        <ul style="list-style-type: none;">
                            {% for  blog_type in blog_types %}
                                <li>
                                    <a href="{% url 'blogs_with_type' blog_type.pk %}">{{ blog_type.type_name }}</a>
                                </li>
                            {% empty %}
                                <li>暂无分类</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

> **模板嵌套**
因为分类的随笔网站样式和博客列表样式类似所以我们直接套用`blog_list`的模板

## `blog_list`

```html
{% extends 'base.html' %}

{% block title %} 我的网站 {% endblock %}
{% block nav_blog_active %}active{%endblock%}

{% load staticfiles %}   加载css文件
{% block header_extends %} 
    <link rel="stylesheet" href= "{% static 'blog/blog.css' %}" >
{% endblock %}



{# 页面内容 #}
{% block content %}
    <div class="container">
        <div class="row">
            <div class=" col-xs-12 col-sm-8 col-md-9 col-lg-10"> 
                <div class="panel panel-default">
                    <div class="panel-heading"> {% block blog_list_title %}博客列表 (一共有{{ blogs|length }}篇博客) {% endblock %}</div>
                    <div class="panel-body">
                        {% for blog in blogs %}
                            <div class="blog">
                                <h3><a href="{% url 'blog_detail' blog.pk %}">{{ blog.title }}</a></h3>
                                    <p class="blog-info">
                                        <span class="glyphicon glyphicon-tag"></span>
                                         <a href="{% url 'blogs_with_type' blog.blog_type.pk %}"> {{ blog.blog_type }}</a>
                                        <span class="glyphicon glyphicon-time"></span>{{ blog.created_time|date:"Y-m-d"}}
                                    </p>
                                <p>{{ blog.content|truncatechars:60}}</p>
                            </div>
                        {% empty %}
                            <div class="blog">
                                <p> <h3>暂无博客，敬请期待</h3></p>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
            <div class=" hidden-xs col-sm-4 col-md-3 col-lg-2"> 
                <div class="panel panel-default">
                    <div class="panel-heading">博客分类</div>
                    <div class="panel-body">
                        <ul class="blog-types">
                            {% for  blog_type in blog_types %}
                                <li>
                                    <a href="{% url 'blogs_with_type' blog_type.pk %}">{{ blog_type.type_name }}</a>
                                </li>
                            {% empty %}
                                <li>暂无分类</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

## `blog_with_type`

```html
{% extends 'blog/blog_list.html' %}

{% block title %}  {{ blog_type.type_name }} {% endblock %}

{% block blog_list_title %} 
    分类：{{ blog_type.type_name }}  
    (一共有{{ blogs|length }}篇博客)
    <a href="{% url 'blog_list' %}"> 查看全部博客 </a>
{% endblock %}

```
> ### CSS

``` css
ul.blog-types {
    list-style-type: none;  去小黑点
}
div.blog:not(:last-child){
    margin-bottom: 2em;
    padding-bottom: 1em;
    border-bottom: 1px solid #eee;
}
div.blog h3 {
    margin-top: 0.5em;
}
div.blog p.blog-info {
    margin-bottom: 0;
}

ul.blog-info-description {
    list-style-type: none;
    margin-bottom: 2em; 下边距
}
ul.blog-info-description li{
    display: inline-block;  所有ul的li标签变成一行
    margin-right: 2em;   每个li标签之间的间距2个字符
}
div.blog-content {
    text-indent: 2em;  首行缩进
}

```
