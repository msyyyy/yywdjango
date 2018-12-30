from django.shortcuts import render,redirect # redirect 跳转
from django.contrib import auth # 登录
from django.urls import reverse # 反向通过别名得到网址
from django.contrib.auth.models import User
from django.http import JsonResponse # 向js返回数据
from .forms import LoginForm, RegForm

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
    return render(request,'user/login.html',context )

       
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
    return render(request,'user/register.html',context )

def logout(request): #登出
    auth.logout(request)
    # 跳转到之前访问的那一页,如果没传进来 返回到首页
    return redirect(request.GET.get('from',reverse('home'))) 

def user_info(request): # 用户个人信息
    context = {}
    return render(request,'user/user_info.html',context)