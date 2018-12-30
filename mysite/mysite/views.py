import datetime
from django.shortcuts import render,redirect # redirect 跳转
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum 
from django.core.cache import cache # 缓存
from django.contrib import auth # 登录
from django.urls import reverse # 反向通过别名得到网址
from django.contrib.auth.models import User
from django.http import JsonResponse # 向js返回数据

from read_statistics.utils import get_seven_days_read_date,get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog
from .forms import LoginForm, RegForm

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

def login(request): # 登录
    if request.method == 'POST': # 如果是提交用户名页面
        login_form = LoginForm(request.POST) # 实例化提交数据
        if login_form.is_valid(): # 如果提交数据有效,这个执行以后会执行froms.py的clean方法,如果是不存在会返回错误
                user = login_form.cleaned_data['user']
                auth.login(request, user) # 存在 登录,有人说login这个会自动提醒如果不正确
                return redirect(request.GET.get('from',reverse('home'))) # 跳转到之前访问的那一页,如果没传进来 返回到首页
    else:                         # 否则是加载页面 
        login_form = LoginForm()
# 数据有效但账号或密码错误  数据无效   在加载页面 都会使用这段代码
    context = {}  
    context['login_form'] = login_form
    return render(request,'login.html',context )

def login_for_medal(request): # 按点赞时能登录
    login_form = LoginForm(request.POST)
    data = {}

    if login_form.is_valid(): 
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

        
def register(request): # 注册
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username,email,password)
            user.save()
            # 最后两步相当于
            # user = User()
            # user.username = username
            # user.email = email
            # user.set_password(password) 保护密码,保存的是加密后密码
            # user.save()
            # 登录用户
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            # 返回到注册页面
            return redirect(request.GET.get('from',reverse('home')))
    else:
        reg_form = RegForm()

    context = {}  
    context['reg_form'] = reg_form
    return render(request,'register.html',context )
