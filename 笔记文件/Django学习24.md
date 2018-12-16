# 使用Django Form 表单

> 作用 : 接收和处理用户提交的数据   可检查提交的数据   可将数据转换成python的数据类型     可自动生成html代码

> 1. 在mysite中新建`forms.py` 创建登录模型

```python
from django import  forms 

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',required=True) # 默认显示为username我们让他显示为用户名 , require 默认为True 这个是如果不没填写用户名他会提醒你
    password = forms.CharField(label='密码',widget=forms.PasswordInput) # 密文输入显示
```
> 2. `blog_detail.html`  博客显示页面点击登录后到登录页面 不过会把自己的链接也上传 方便登陆后返回

```html
您尚未未登录,登录之后方可评论~
<a href="{% url 'login' %}?from={{ request.get_full_path }}">登录</a>
 <!--?from={{ request.get_full_path }}把从哪里来的链接发送进去登录以后可以跳转回来-->
```

> 3. `mysite/views.py` 登录判断

```python
def login(request): # 登录
    '''旧代码
    username = request.POST.get('username','') # 传进来POST是字典形式 如果获取不到username 设置为''(空)
    password = request.POST.get('password','')
    user = auth.authenticate(request, username=username,password=password) # 验证数据库中是否有对应账号密码
    referer =  request.META.get('HTTP_REFERER', reverse('home')) # 获取是从哪个网址跳转过来的 如果获取不到 那么返回首页(通过别名反向得到链接)
    if user is not None: 
        auth.login(request, user) # 存在 登录,有人说login这个会自动提醒如果不正确
        return redirect(referer) # 跳转到之前访问的那一页
    else:
        return render(request, 'error.html',{'message':'用户名或密码不正确','redirect_to': referer }) # 验证失败 跳转到错误页面
    '''
    if request.method == 'POST': # 如果是提交用户名页面
        login_form = LoginForm(request.POST) # 实例化提交数据
        if login_form.is_valid(): # 如果提交数据有效
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password'] # 获取填写的账号密码
            user = auth.authenticate(request, username=username,password=password) # 验证数据库中是否有对应账号密码
            if user is not None:  # 如果存在
                auth.login(request, user) # 存在 登录,有人说login这个会自动提醒如果不正确
                return redirect(request.GET.get('from',reverse('home'))) # 跳转到之前访问的那一页,如果没传进来 返回到首页
            else:
                login_form.add_error(None,'用户名或密码不正确') # 不存在,增加错误信息 再返回回去，返回到提交用户名的页面
    else:                         # 否则是加载页面 
        login_form = LoginForm()
# 数据有效但账号或密码错误  数据无效   在加载页面 都会使用这段代码
    context = {}  
    context['login_form'] = login_form
    return render(request,'login.html',context )
```

> 4. `mysite/templates/login.html` 登录页面

```html
{% extends 'base.html' %}
{% load staticfiles %}

{% block title %}
        我的网站|登录
{% endblock %}

{% block nav_home_active %}
    active
{%endblock%}


{% block content %}
    <form action="" method="POST"> <!--弹出文本框，因为是传送到当前页面所以action为""-->
        {% csrf_token %}   <!--csrf令牌 安全性-->
        {{ login_form }}

        <input type="submit" value="登录"> <!--submit是按钮  发生数据至上面action的网址-->
    </form>
{% endblock %}
```

> 注册
> 1. urls 注册

> 2. `froms.py` 增加注册模型

```python
# 注册
class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                                max_length=30,
                                min_length=3,
                               widget=forms.TextInput(
                                            attrs={'class':'form-control','placeholder':'请3-30位输入用户名'}))
    email = forms.CharField(label='邮箱',
                               widget=forms.EmailInput(
                                            attrs={'class':'form-control','placeholder':'请输入邮箱'}))
    password  = forms.CharField(label='密码',
                                min_length=6,
                               widget=forms.PasswordInput(
                                            attrs={'class':'form-control','placeholder':'请输入密码'}))
    password_again  = forms.CharField(label='再输入一次密码',
                                        min_length=6,
                                        widget=forms.PasswordInput(
                                            attrs={'class':'form-control','placeholder':'再一次输入密码'}))

    # 判断用户名是否被注册
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    # 判断邮箱已被注册
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    # 验证两遍密码是否一致
    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password !=password_again:
            raise forms.ValidationError('两次密码不一致')
        return password

```

> 3. `mysite/view.py` 增加注册的方法

```python
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
    
```

> 4. 增加 注册的html   `register.html`

```html
{% extends 'base.html' %}
{% load staticfiles %}

{% block title %}
        我的网站|注册
{% endblock %}

{% block nav_home_active %}
    active
{%endblock%}


{% block content %}
    <div class="containter">
        <div class="row">
            <div class="col-xs-4 col-xs-offset-4">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h3 class="panel-title">注册</h3>
                    </div>
                    <div class="panel-body">
                        <form action="" method="POST">
                            {% csrf_token %}
                            {% for field in reg_form %}
                                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                                {{ field }}
                                <p class="text-danger">{{ field.errors.as_text }}</p>
                            {% endfor %}
                            <span class="pull-left text-danger">{{ reg_form.non_field_errors }}</span>
                            <input type="submit" value="注册" class="btn btn-primary pull-right">
                        </form>
                    </div>
                </div>                
            </div>
        </div>
    </div> 
{% endblock %}

```
> 5. 在博客页面显示登录按钮 `blog_detail.html`

```html
您尚未未登录,登录之后方可评论~
<a class="btn btn-primary" href="{% url 'login' %}?from={{ request.get_full_path }}">登录</a> <!--?from={{ request.get_full_path }}把从哪里来的链接发送进去登录以后可以跳转回来-->
<span>or</span>
<a class="btn btn-danger" href="{% url 'register' %}?from={{ request.get_full_path }}">注册</a> 
```
