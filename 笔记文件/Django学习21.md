# 热门博客阅读及缓存提速

> 利用阅读量数据排行

> 1. 当天阅读数据排行
`read_statistics/utils.py`
```python
def get_today_hot_data(content_type):  # 获取今天的热门文章
    today = timezone.now().date()
    read_details  = ReadDetail.objects.filter(content_type=content_type,date=today)
    return read_details.order_by('-read_num') # 由阅读数 倒叙排序(有大到小)  
```
`read_statistics/views.py`

```python
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_date, get_today_hot_data
from blog.models import Blog
def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog) # 获得关联到Blog类型的 ContentType实例
    dates,read_nums = get_seven_days_read_date(blog_content_type)    # 获得前七天博客阅读的元组
    today_hot_data = get_today_hot_data(blog_content_type)   # 获得今天热门博客的元组

    context={}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data
    return render_to_response('home.html',context)
```
