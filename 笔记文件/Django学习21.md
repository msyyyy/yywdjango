# 热门博客阅读及缓存提速

> 利用阅读量数据排行

> 1. 当天阅读数据排行
`read_statistics/utils.py`
```python
def get_today_hot_data(content_type): # 获取今天的热门博客
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')# 先找出符合条件的ReadDetail 在由read_num 从大到小排序
    return read_details[:7] # 切片 取前7条
```
`read_statistics/views.py`

```python
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_date,get_today_hot_data
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog) # 获得关联到Blog类型的 ContentType实例
    dates,read_nums = get_seven_days_read_date(blog_content_type)    # 获得前七天博客阅读的list
    today_hot_data = get_today_hot_data(blog_content_type) # 获取今天热门博客

    context={}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    return render_to_response('home.html',context)
```
`home.html`
```html
<h3>今天热门博客</h3>
    <ul>
        {% for hot_data in today_hot_data %}
            <li><a href="{% url 'blog_detail' hot_data.content_object.pk %}">{{ hot_data.content_object.title }}</a>
             ({{ hot_data.read_num }})</li>
        {% empty %}
            <li>今天暂无热门博客</li>
        {% endfor %}
    </ul>
```

> 获取7天内热门博客

`utils.py`
```python
def get_7_hot_data(content_type): # 获取7天内热门博客
    today = timezone.now().date()
    date= today -datetime.timedelta(days=7) # 7天前
    read_details = ReadDetail.objects \
                             .filter(content_type=content_type,date__lt=today,date__gte=date) \
                             .order_by('-read_num')# 得到7天前到今日这个范围内的日期
    return read_details[:7]
```

不过 还是有问题 比如如果前几天中有篇博客经常阅读量靠前 可能会经常出现同一篇  我们要做的是分组统计  把7天的数据累加起来 高的靠前

`utils.py`
```python
def get_7_hot_data(content_type): # 获取7天内热门博客
    today = timezone.now().date()
    date= today -datetime.timedelta(days=7) # 7天前
    read_details = ReadDetail.objects \
                             .filter(content_type=content_type,date__lt=today,date__gte=date) \
                             .values('content_type','object_id') \     分组 按 content_type 和 object_id分
                             .annotate(read_num_sum=Sum('read_num')) \ 统计 每个组的阅读记录和
                             .order_by('-read_num_sum')# 按每个组的记录和 有大到小排序
    return read_details[:7]
```
`mysite\views.py`
```python
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_date,get_today_hot_data, get_yesterday_hot_data, get_7_hot_data
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog) # 获得关联到Blog类型的 ContentType实例
    dates,read_nums = get_seven_days_read_date(blog_content_type)    # 获得前七天博客阅读的list

    context={}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type) # 获取今天热门博客
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type) # 获取昨天热门博客
    context['hot_data_for_7_days'] = get_7_hot_data(blog_content_type) # 获取7日内热门博客  已经按7天内阅读数之和排序
    return render_to_response('home.html',context)

```
`home.html`
```html
<h3>7天热门博客</h3>
    <ul>
        {% for hot_data in hot_data_for_7_days %}
            <li><a href="{% url 'blog_detail' hot_data.object_id %}">xxx</a> 有个问题 这里无法用hot_data.content_object.titlex显示标题
             ({{ hot_data.read_num_sum }})</li>
        {% empty %}
            <li>7天内暂无热门博客</li>
        {% endfor %}
    </ul>
```

出现了上面的问题  所有我们得用新方法解决 分组计数

### Blog反向关联到ReadDetail
`blog\models.py`
```python
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation # 反向关联
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail # 引入ReadDetail

class BlogType (models.Model):
    type_name = models.CharField(max_length=15)

    def __str__ (self):  #让文章选择分类时能看到分类名
        return self.type_name
    def blog_count(self): 
        return self.blog_set.count()  # blog_set 反向获取被关联外键的model（模型名称小写加_set）

class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING) # 删除博客对博客类型无影响  多对一
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)  # 反向关联到ReadDetail    关联以后直接 blog.read_details.all()就能查看该博客所有readdetail
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']  # 按时间排序  最新的在最前

```

`mysite\views.py`
```python
import datetime
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum 
from read_statistics.utils import get_seven_days_read_date,get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog

def get_7_days_hot_blogs():  # 获取7天内热门博客
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \ 
                .filter(read_details__date__lt=today, read_details__date__gte=date) \  访问Blog反关联模型 通过 __连接
                .values('id','title') \  分组
                .annotate(read_num_sum=Sum('read_details__read_num')) \ 统计和
                .order_by('-read_num_sum')  # 排序
    return blogs
    

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog) # 获得关联到Blog类型的 ContentType实例
    dates,read_nums = get_seven_days_read_date(blog_content_type)    # 获得前七天博客阅读的list

    context={}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type) # 获取今天热门博客
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type) # 获取昨天热门博客
    context['hot_blogs_for_7_days'] = get_7_days_hot_blogs() # 获取7日内热门博客  已经按7天内阅读数之和排序
    return render_to_response('home.html',context)
```
`home.html`
```html
<h3>7天热门博客</h3>
    <ul>
        {% for hot_blog in hot_blogs_for_7_days %}
            <li><a href="{% url 'blog_detail' hot_blog.id %}">{{ hot_blog.title }}</a>
             ({{ hot_blog.read_num_sum }})</li>
        {% empty %}
            <li>7天内暂无热门博客</li>
        {% endfor %}
    </ul>
```

> 有些数据经常计算 耗时 怎么去缓存数据 ，因为昨天 和前7天的数据其实是固定的 我们只要隔一定时间刷新就行

内存缓存 Memcached   Redis
数据库缓存
文件缓存

> 我们这边选的是数据库缓存

> 1. ` settings.py `
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
```
> 2. 在使用数据库缓存之前得创建缓存表 python manage.py createcachetable

> 3. `mysite\views.py` 获取缓存
```python
import datetime
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum 
from django.core.cache import cache # 缓存
from read_statistics.utils import get_seven_days_read_date,get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog


def get_7_days_hot_blogs():  # 获取前7天内热门博客
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id','title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]
    

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog) # 获得关联到Blog类型的 ContentType实例
    dates,read_nums = get_seven_days_read_date(blog_content_type)    # 获得前七天博客阅读的list

    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:   # 如果获取不到 那么 得到None 需要重新计算
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days',hot_blogs_for_7_days,3) # 存放缓存  先是一个字典  然后是有效期(以s为单位)

    context={}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type) # 获取今天热门博客
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type) # 获取昨天热门博客
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days # 获取7日内热门博客  已经按7天内阅读数之和排序
    return render_to_response('home.html',context)
```
