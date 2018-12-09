# 博客分类统计

> 想统计每个类型的博客到底有几篇 显示出来

> 1. 方法一 
## `views.py`
```python
# 获取博客分类的对应博客数目
    blog_types = BlogType.objects.all() # 获取所有博客分类
    blog_types_list = []       
    for blog_type in blog_types:
        # 给 blog_type 这个BlogType的实例 加入了新的属性 .blog_count  这里的意思是 Blog.blog_type = blog_type 
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count() 
        blog_types_list.append(blog_type) 

    context = {}
    context['blog_types'] = blog_types_list
```
## `blog_list.html`
```html
<div class="panel-body">
    <ul class="blog-types">
        {% for  blog_type in blog_types %}
            <li>
                <a href="{% url 'blogs_with_type' blog_type.pk %}">
                    {{ blog_type.type_name }} ({{ blog_type.blog_count }})
                </a>
            </li>
        {% empty %}
            <li>暂无分类</li>
        {% endfor %}
    </ul>
</div>
```

> 2. 方法二 通过annotate拓展查询字段方法

## ‘blog_list.html`还是原样修改

## `views.py`
```python
from django.db.models import Count  # 引用
# 获取博客分类的对应博客数目，和上面一段话效果一样

context['blog_types'] = BlogType.objects.annotate( blog_count = Count('blog')) # SQL语句等访问时再执行 Blog通过外键相关连了BlogType，返回与每个不同标签外键的博客数

```

> 3. 方法三  拓展BlogType的方法

## `models.py`
```python
class BlogType (models.Model):
    type_name = models.CharField(max_length=15)

    def __str__ (self):  #让文章选择分类时能看到分类名
        return self.type_name
    def blog_count(self): 
        return self.blog_set.count()  # blog_set 反向获取被关联外键的model（模型名称小写加_set）
```
## `views.py`
```python
context['blog_types'] = BlogType.objects.all()
```
## `blog_list.html`
```html
<div class="panel panel-default">
    <div class="panel-heading">博客分类</div>
    <div class="panel-body">
        <ul class="blog-types">
            {% for  blog_type in blog_types %}
                <li>
                    <a href="{% url 'blogs_with_type' blog_type.pk %}">
                        {{ blog_type.type_name }} ({{ blog_type.blog_count }}) <!-- 调用BlogType的 blog_count 方法 -->
                    </a>
                </li>
            {% empty %}
                <li>暂无分类</li>
            {% endfor %}
        </ul>
    </div>
</div>
```

> 同理 想统计每个日期 的博客到底有几篇 显示出来

## `views.py`
```python
# 获得日期归档对应的博客数量
blog_dates =  Blog.objects.dates('created_time','month',order="DESC")
blog_dates_dict = {}   # 字典,相当于c++map
for blog_date in blog_dates:
    #找出所有存在的年月 的博客数量
    blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                        created_time__month=blog_date.month).count()
    blog_dates_dict[blog_date] = blog_count  # 将年月和博客数量对应

context['blog_dates'] = blog_dates_dict 
```
## `blog_list.html`
```html
<div class="panel panel-default">
    <div class="panel-heading">日期归档</div>


    <div class="panel-body">
        <ul>
            {% for blog_date, blog_count in blog_dates.items %}  <!-- 现在这里是字典  循环字典blog_dates.items 得到 键值 和 权值-->
                <li>
                    <a href="{% url 'blogs_with_date' blog_date.year blog_date.month %}">
                        {{ blog_date|date:"Y年m月" }} ({{ blog_count }})
                    </a>
                </li> 
            {% endfor %}
        </ul>
    </div>
</div>
```
