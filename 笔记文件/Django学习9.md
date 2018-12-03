

## 常用模板标签

1. 在templates文件夹下创建base.html
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>{% block title %} {% endblock %} </title> {# 模块 #}
</head>
<body>
    <div>
        <a href={% url 'home' %}>
            <h3>个人博客网站</h3>
        </a>  
    </div>
    <hr>
    {% block content %} {% endblock %}  {# 模块 #}
</body>
</html>
```
2. 其他html文件
```html
{% extends 'base.html' %} {# 引用base.html文件 #}

{% block title %}    {# 插入原title #}
    {{ blog.title }}
{% endblock %}

{% block content %}
    <h3>{{ blog.title }}</h3>
    <p>作者:{{ blog.author }} </p>
    <p>发表日期: {{ blog.created_time|date:"Y-m-d G:n:s" }}</p>
    <P>分类: 
        <a href="{% url 'blogs_with_type' blog.blog_type.pk %}">
            {{ blog.blog_type }}
        </a>
    </P>
    <p>{{ blog.content }}</p>
{% endblock %}

```
## 全局模板文件夹
>1. 在主mysite文件夹下创建templates 文件夹
>2. 在mysite文件的setting文件
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates'),
            #BASE_DIR 代表主mysite的地址
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
>3. 将处于blog中的base文件转移到  templates 文件夹
 templates 文件夹创建 blog文件夹 将模板文件都放入其中
 


