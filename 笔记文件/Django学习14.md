# 优化分页展示

> 当前页高亮
## `blog_list.html`
```html
<!-- 全部页码 -->
{% for page_num in page_of_blogs.paginator.page_range %}  <!-- page_of_blogs.paginator  代表该分页对应的总分页 page_range 输出的是 1   2   3  4这样 -->
    {% if page_num == page_of_blogs.number %}       
        <li class= "active"><a href="?page={{ page_num }}">{{ page_num }}</a></li>  class ="active" 应该是高亮
    {% else %}
        <li><a href="?page={{ page_num }}">{{ page_num }}</a></li>
    {% endif %}
    
{% endfor %}   
```

paginator.num_pages  最后页

> 不要过多页码选择，影响页面布局

## `views.py`
```python
def blog_list(request):

    blogs_all_list=Blog.objects.all()
    paginator = Paginator(blogs_all_list,5) # 每5篇进行分页
    page_num = request.GET.get('page',1) # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num) # 如果得到的是非法页码自动返回 1
    currentr_page_num = page_of_blogs.number # 获取当前页码
    page_range=[x for x in range(int(page_num)-2, int(page_num)+3  )  if 0<x<=paginator.num_pages] # 获取当前页的前两页 和 后两页
    

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs  # 传入分页信息
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html',context)
```
## `blog_list.html`
```html
{% for page_num in page_range %} 
{% if page_num == page_of_blogs.number %}
    <li class= "active"><span>{{ page_num }}</span></li>
{% else %}
    <li><a href="?page={{ page_num }}">{{ page_num }}</a></li>
{% endif %}

{% endfor %}   
```



`css`
div.paginator {
    text-align: center;  居中
}

> 更方便的修改每个页存在的博客篇数

> 1. settings中增加参数
```python
# 自定义参数 每个分页显示博客数量
EACH_PAGE_BLOGS_NUMBER = 7
```
> 2. views中引用
```python
from django.conf import settings
paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) # 每几篇文章进行分页
```
