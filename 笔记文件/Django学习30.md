# 导航栏添加用户操作

登录 注册 登出

> 1. 导航栏右侧添加 登录/注册  或 用户信息

bootstrap 导航栏

`mysite/urls.py` 路由设置

```python
path('logout/',views.logout, name='logout'), # 登出
path('user_info/',views.user_info, name='user_info'), # 用户个人信息
```


`base.html` 前段网页设置

```html
<ul class="nav navbar-nav navbar-right"><!--登录注册或者显示用户状态-->
    {% if not user.is_authenticated %} <!--未登录-->
            <!--?from={{ request.get_full_path }}把从哪里来的链接发送进去登录以后可以跳转回来-->
        <li>
            <a href="{% url 'login' %}?from={{ request.get_full_path }}">登录</a>
        </li>
        <li>
            <a href="{% url 'register' %}?from={{ request.get_full_path }}">注册</a>
        </li>
    {% else %}
        <li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{{ user.username }} <span class="caret"></span></a>
        <ul class="dropdown-menu">
            <li><a href="{% url 'user_info' %}">个人资料</a></li>
            <li role="separator" class="divider"></li> <!--分割线-->
            <li><a href="{% url 'logout' %}?from={{ request.get_full_path }}">登出</a></li>
        </ul>
        </li>
    {% endif %}
</ul>
```

`mysite/views.py`  创建模型
```python
def logout(request): #登出
    auth.logout(request)
    # 跳转到之前访问的那一页,如果没传进来 返回到首页
    return redirect(request.GET.get('from',reverse('home')))

def user_info(request): # 用户个人信息
    context = {}
    return render(request,'user_info.html',context)
```

`templates/user_info.html`   个人资料页面

```html
{% extends 'base.html' %}

{% block title %}个人资料{% endblock %}
{% block nav_home_active %}active{%endblock%}


{% block content %}
<div class="containter">
    <div class="row">
        <div class="col-xs-10 col-xs-offset-1">
            {% if user.is_authenticated %} <!--已登录-->
                <h2>{{ user.username }}</h2> 
                <ul>
                    <li>昵称: <a href="#">修改昵称</a></li>
                    <li>邮箱: {% if user.email %} {{ user.email }} {% else %}未绑定 <a href="#">绑定邮箱</a>{% endif %}</li>
                    <li>上一次登录的时间: {{ user.last_login|date:"Y-m-d H:i:s" }}</li>
                    <li><a href="#">修改密码</a></li>
                </ul> 
            {% else %}
                <span>未登录,跳转到首页.....</span>
                <script type="text/javascript">
                    window.location.href = '/'; // 跳转到首页
                </script>
            {% endif %}
        </div>
    </div>
</div> 
{% endblock %}

```

>  创建 user   app 把关于用户的模型和方法都放入其中,降低耦合性

> 将弹出登录页面模块化

创建 `user/context_processors`

```python
from .forms import LoginForm

def login_modal_form(request):
    return {'login_modal_form': LoginForm()}
```

在 `mysite/settings`加入
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates'),
            
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'user.context_processors.login_modal_form', # 新增这一句 
            ],
        },
    },
]
```

应用时 `bolg_detail.html`

```html
{% for field in login_modal_form %}   <!-- 改用login_modal_form -->
    <label for="{{ field.id_for_label }}">{{ field.label }}</label>
    {{ field }}
{% endfor %}
```


> 将弹窗登录 迁移到`base.html`中

