import datetime
from django.shortcuts import render,redirect # redirect 跳转
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum 
from django.core.cache import cache # 缓存
from django.urls import reverse # 反向通过别名得到网址
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
    return render( request,'home.html',context)
