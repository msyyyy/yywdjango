   # CSS美化页面

> 新增home界面

`home.html`
```html
{% extends 'base.html' %}

{% block title %}
        我的网站|首页
{% endblock %}

{% block content %}
    <h3 class="home-content"> 欢迎访问我的网站~~</h3>
    
    <style type="text/css"> {# css 美化 #}
        h3.home-content {  访问h3标签下的"home-content"类
            font-size: 222%;
            position: absolute;绝对位置
            left: 50%; 从左到右50%的位置
            top: 50%;  
            transform: translate(-50%,-50%); 再回去一半
        }
    </style>
{% endblock %}
```
> 我的网站|首页的美化

>方法一

`base.html`
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>{% block title %} {% endblock %} </title>
    <link rel="stylesheet" href="/static/base.css"> 
    我将css代码做成css文件放在了主mysite下static文件夹下名字为base.css
    不过要使用这个得修改settings.py文件
</head>
<body>
    <div class= "nav" >
        <a class="logo" href={% url 'home' %}>
            <h3>个人博客网站</h3>
        </a>  
        <a href= '/'> 首页  </a>
        <a href= {% url 'blog_list' %}> 博客 </a>
    </div>
    <hr>
    {% block content %} {% endblock %}

</body>
</html>
```

`settings.py`
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
] 
可以使用static下的文件
在网页中能通过 localhost:8000/static/base.css访问base.css文件的内容
```
`base.css`
```css
* {  *号使得没有浏览器的默认
    margin: 0; 外间距
    padding: 0; 内间距
}
div.nav {
    background-color: #eee;
    border-bottom:1px solid #ccc;
    padding: 10px 5px;
}
div.nav a{
    text-decoration: none;
    color: #000;
    padding: 5px 10px;
} 
div.nav a.logo {
    display: inline-block;
    font-size: 120%;
}
```

> 方法二

`base.html `
```html
{% load staticfiles %}  新增引用

<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>{% block title %} {% endblock %} </title>
    现 <link rel="stylesheet" href="{% static 'base.css'%}"> 
    原 <link rel="stylesheet" href="/static/base.css"> 
</head>
<body>
    <div class= "nav" >
        <a class="logo" href={% url 'home' %}>
            <h3>个人博客网站</h3>
        </a>  
        <a href= '/'> 首页  </a>
        <a href= {% url 'blog_list' %}> 博客 </a>
    </div>
    <hr>
    {% block content %} {% endblock %}

</body>
</html>
```

> 为了便于css的使用修改base

```html
{% load staticfiles %}

<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>{% block title %} {% endblock %} </title>
    <link rel="stylesheet" href="{% static 'base.css'%}">
    {% block header_extends %}  {% block endblock %}  新增css块
</head>
<body>
    <div class= "nav" >
        <a class="logo" href={% url 'home' %}>
            <h3>个人博客网站</h3>
        </a>  
        <a href= '/'> 首页  </a>
        <a href= {% url 'blog_list' %}> 博客 </a>
    </div>
    <hr>
    {% block content %} {% endblock %}

</body>
</html> 
```
`home.html`
```html
{% extends 'base.html' %}
{% load staticfiles %} 还需要加载

{% block title %}
        我的网站|首页
{% endblock %}

{% block header_extends %}
    <link rel="stylesheet" href="{% static 'home.css' %}">
{% endblock %}

{% block content %}
    <h3 class="home-content"> 欢迎访问我的网站~~</h3>
{% endblock %}
```

> # bootstrap库
已经写好的css库