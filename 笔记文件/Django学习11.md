# css框架 bootstrap
## [bootstrap官网](http://www.bootcss.com/)

`base.html`

```html
{% load staticfiles %} 

<!DOCTYPE html>
<html lang="zh-CN"> {# 中文 #}
<head>
    <meta charset='UTF-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> {# IE浏览器访问 #}
    <meta name="viewport" content="width=device-width, initial-scale=1"> {# 根据不同屏幕自动响应布局 #}
    <title>{% block title %} {% endblock %} </title>

    <link rel="stylesheet" href="{% static 'base.css' %}"> 加载css美化文件
    <link rel="stylesheet" href="{% static 'bootstrap-3.3.7/css/bootstrap.min.css' %}">
    
    <script type="text/javascript" src="{% static 'jquery-1.12.4.min.js' %}"></script>  jquery这个要放在前面
    <script type="text/javascript" src="{% static 'bootstrap-3.3.7/js/bootstrap.min.js' %}"></script>
    {% block header_extends %}  {% endblock %}
</head>
<body>
    {# 导航栏 #}
    <div class="navbar navbar-default" role="navigation"> 
        <div class="container-fluid">
            <div class="navbar-header" >
                <a class="navbar-brand" href="{% url 'home' %}">个人博客网站
                </a>
                <button class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar-collapse">  {# 按钮 #}
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    有三行这个代表按钮有三个横杠
                </button>
            </div>
            <div id="navbar-collapse" class="collapse navbar-collapse" >  {# 对应上一个按钮的下拉列表 #}

                中途遇到下拉标签点击无效 发现是 当前 id打错了 之前打的是id="navbar_collapse"未和上面的按钮data-target相同
                <u1 class="nav navbar-nav">
                    <li><a href="{% url 'home' %}">首页</a></li>
                    <li><a href="{% url 'blog_list' %}">博客</a></li>
                    写了两个 下拉就有两个
                </u1>
            </div>
        </div>
    </div>

    {% block content %} {% endblock %}

</body>
</html> 
```

> 显示访问到哪 那里被激活
`base.html`
```html
<u1 class="nav navbar-nav">
    <li class="{% block nav_home_active %} {% endblock %}">
        <a href="{% url 'home' %}">首页</a>
    </li>
    <li class="{% block nav_blog_active %} {% endblock %}">
        <a href="{% url 'blog_list' %}">博客</a>
    </li>
</u1>
```
`hmoe.html`
```html
{% extends 'base.html' %}
{% load staticfiles %}

{% block title %}
        我的网站|首页
{% endblock %}

{% block header_extends %}
    <link rel="stylesheet" href="{% static 'home.css' %}">
{% endblock %}

{% block nav_home_active %}   激活了home
    active                
{%endblock%}


{% block content %}
    <h3 class="home-content"> 欢迎访问我的网站~~</h3>
{% endblock %}
```
其他.html
```html
{% block nav_blog_active %}   激活了home
    active                
{%endblock%}
```
> 让导航栏一直停留在页面顶部

{# 导航栏 #}
<div class="navbar navbar-default navbar-fixed-top" role="navigation"> 多加一条 navbar-fixed-top 即可
这样有个问题 他会挡住文章标题 我们得预留导航栏宽度
`base.css`
```css
* {
margin: 0;
padding: 0;
}
body {
    margin-top: 70px!important; 不加!important 不行 
}
```