# 上下篇博客和按月分类

## 对比当前博客得到上一篇和下一篇
```

filter筛选 符合条件的 返回 QuerySet

等于 直接筛选
大于 __gt
大于等于  __gte
小于  __lt
小于等于 __lte
包含 __contains (加 i 忽略大小写)
开头是 __startswith
结尾是 __endswith
其中之一 __in
范围 __range  （如 __range(1,5)）

exclude 排除条件 

用法和filter一样 相当于filter取反

```
## 条件中的双下划线
> 字段查询类型

> 外键拓展

> 日期拓展
如 Blog.objects.filter(created_time__year=2017)  # 查询了博客中创建日期为2017年的

> 支持链式查询

## 新增博客日期分类

> 1. 新增 `urls.py`
```python
path('date/<int:year>/<int:month>',views.blogs_with_date,name="blogs_with_date"),
```

> 2. `views.py` 在博客列表里加入日期归档
```python
def blog_list(request):
    blogs_all_list=Blog.objects.all()
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) # 每几篇文章进行分页
    page_num = request.GET.get('page',1) # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num) # 如果得到的是非法页码自动返回 1
    currentr_page_num = page_of_blogs.number # 获取当前页码
    page_range=[x for x in range(int(page_num)-2, int(page_num)+3  )  if 0<x<=paginator.num_pages] # 获取当前页的前后两页

    
    if page_range[0] -1 >=2:   # 加上省略号
        page_range.insert(0,'...')
    if paginator.num_pages -page_range[-1] >=2:
        page_range.append('...')

    if page_range[0] !=1:   # 如果page_range没有1号页码 增加一个1号页码按钮
        page_range.insert(0,1)
    if page_range[-1] !=paginator.num_pages:     # 如果page_range没有最后页码 
        page_range.append (paginator.num_pages)

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs  # 传入分页信息
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time','month',order="DESC") #字段  类型  排序
    # mouth 返回的是year和month    DESC 由新到旧  获得日期的分类
    return render_to_response('blog/blog_list.html',context)
```

> 3. `blog_list.html` 
```html
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
    <div class="panel panel-default">
        <div class="panel-heading">日期归档</div>
        <div class="panel-body">
            <ul>
                {% for blog_date in blog_dates %}
                    <li>
                        <a href="{% url 'blogs_with_date' blog_date.year blog_date.month %}">
                            {{ blog_date|date:"Y年m月" }}
                        </a>
                    </li> 
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
```

> `views.py`  blogs_with_date
```python
def blogs_with_date(request,year,month):
    
    blogs_all_list=Blog.objects.filter(created_time__year=year,created_time__month=month)
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) 
    page_num = request.GET.get('page',1) # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num) # 如果得到的是非法页码自动返回 1
    currentr_page_num = page_of_blogs.number # 获取当前页码
    page_range=[x for x in range(int(page_num)-2, int(page_num)+3  )  if 0<x<=paginator.num_pages] # 获取当前页的前后两页

    
    if page_range[0] -1 >=2:   # 加上省略号
        page_range.insert(0,'...')
    if paginator.num_pages -page_range[-1] >=2:
        page_range.append('...')

    if page_range[0] !=1:   # 如果page_range没有1号页码 增加一个1号页码按钮
        page_range.insert(0,1)
    if page_range[-1] !=paginator.num_pages:     # 如果page_range没有最后页码 
        page_range.append (paginator.num_pages)

    context = {}
    context['blogs_with_date'] = '%s年%s月' % (year,month)
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs  # 传入分页信息
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('created_time','month',order="DESC")
    context['blog_types'] = BlogType.objects.all()

    return render_to_response('blog/blogs_with_date.html',context)
```

> `blogs_with_date.html`
```html
{% extends 'blog/blog_list.html' %}

{% block title %}  {{ blog_type.type_name }} {% endblock %}

{% block blog_list_title %} 
    日期归档：{{ blogs_with_date }}  
{% endblock %}
```

## views.py文件中的类型有很多重复代码

```python
from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator #分页器
from .models import Blog,BlogType
from django.conf import settings

def get_blog_list_common_date(request,blogs_all_list): # 重复部分写成函数到时候调用
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) # 每几篇文章进行分页
    page_num = request.GET.get('page',1) # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num) # 如果得到的是非法页码自动返回 1
    currentr_page_num = page_of_blogs.number # 获取当前页码
    page_range=[x for x in range(int(page_num)-2, int(page_num)+3  )  if 0<x<=paginator.num_pages] # 获取当前页的前后两页

    
    if page_range[0] -1 >=2:   # 加上省略号
        page_range.insert(0,'...')
    if paginator.num_pages -page_range[-1] >=2:
        page_range.append('...')

    if page_range[0] !=1:   # 如果page_range没有1号页码 增加一个1号页码按钮
        page_range.insert(0,1)
    if page_range[-1] !=paginator.num_pages:     # 如果page_range没有最后页码 
        page_range.append (paginator.num_pages)

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs  # 传入分页信息
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time','month',order="DESC") #字段  类型  排序
    # mouth 返回的是year和month    DESC
    return context

def blog_list(request):
    blogs_all_list=Blog.objects.all()
    context = {}
    context = get_blog_list_common_date(request,blogs_all_list)
    return render_to_response('blog/blog_list.html',context)


def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list=Blog.objects.filter(blog_type=blog_type)
    context = {}
    context = get_blog_list_common_date(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    blogs_all_list=Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = {}
    context = get_blog_list_common_date(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year,month)
    return render_to_response('blog/blogs_with_date.html',context)

def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog,pk=blog_pk)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() # 获取上一篇博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 获取下一篇博客 
    context['blog'] = blog
    return render_to_response('blog/blog_detail.html',context)

```