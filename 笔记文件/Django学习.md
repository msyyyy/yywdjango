
> python manage.py startapp 应用名称
> 创建一个app

 title = models.CharField(max_length = 30) 标题，最长30
 content = models.TextField() 文章内容

#####同步到数据库
> 需要执行 makemigrations    -> 制造迁移
>        migrate   -> 迁移

但是在makemigrations之前你要先去setting 文件声明

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'article',
]
```

> runserver 执行本地服务

全局语言设置在setting文件中 
LANGUAGE_CODE = 'zh-Hans' 中文代码 zh-Hans


想把 Article显示到网站上
进入 article 中的admin.py文件

```python
from .models import Article  先从models把Aeticle 类引用


admin.site.register(Article) 
```
###视频四
**怎么通过一个处理方法去响应不同文章**

> 通过文章的唯一标识id 
> views一般是处理响应的,怎么输出

``` python
1.先在views文件中输入  `相应方法和输出`
from django.http import HttpResponse   #头文件

def article_detail(request,article_id): 
    return HttpResponse("文章id: %s" % article_id)
```

> urls 规定哪些网址可用 

```python
from article.views import article_detail #引用方法

path('article/<int:article_id>',article_detail,name="article_detail"),
```
> 将文章标题输出
``` python
# article下views.py文件

from django.shortcuts import render
from django.http import HttpResponse
from .models import Article #引用模型

# Create your views here.
def article_detail(request,article_id):
    article =Article.objects.get(id=article_id) 

   #模型的object 是获取或操作模型的对象
   # Article.objects.get(条件)
   # Article.objects.all()
   # Article.objects.filter(条件)

    return HttpResponse("文章标题: %s" % article.title)

```
> 文章内容输出
```
<br> 代表换行
<h2>   标题+内容        </h2> 标题+内容字体大小为 h2

```
> 我们现在只有3篇文章但是要访问第5篇就会报错 
```python
from django.shortcuts import render
from django.http import HttpResponse,Http404
from .models import Article

# Create your views here.
def article_detail(request,article_id):
    try:
        article =Article.objects.get(id=article_id)
    except Article.DoesNotExist: #如果出现这个不存在该文章错误输出不存在
        return HttpResponse("不存在") # 或者直接返回404   raise Http404("文章不存在")
    return HttpResponse("<h2>文章标题: %s </h2> <br> 文章内容: %s" % (article.title,article.content))

```
#####使用模版
前段页面和后端代码分离 降低耦合性
后端 先在article创建`templates文件夹`   在其中创建`article_detail.html文件`
``` html
<html>
<head>
</head>
<body>
    <h2>{{ article_obj.title }}</h2>
    <hr> <!--<hr>代表横线-->
    <p>{{ article_obj.content }}</p>
</body>
</html>

```
views文件
```python
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404
from .models import Article

# Create your views here.
def article_detail(request,article_id):
    try:
        article =Article.objects.get(id=article_id)
        context = {} #字典
        context['article_obj']=article
        #return render(request,"article_detail.html",context)
        return render_to_response("article_detail.html",context)
        #上面两个效果一样
    except Article.DoesNotExist:
        raise Http404("文章不存在")
    #return HttpResponse("<h2>文章标题: %s </h2> <br> 文章内容: %s" % (article.title,article.content))

```
get_object_or_404()可以直接看是否不存在
```python
from django.shortcuts import render,render_to_response,get_object_or_404
from django.http import HttpResponse,Http404
from .models import Article

# Create your views here.
def article_detail(request,article_id):
    article =get_object_or_404(Article,pk=article_id)
    context = {}
    context['article_obj']=article
    return render_to_response("article_detail.html",context)
```
#####获取文章列表
所以还是在三个文件做改动
> 1.新增templates文件夹下`article_list.html`文件
> 2.article文件夹下  `views.py`新增 `article_list方法`
> 3.mysite 文件夹下 `urls.py` 加入新网址格式
> path('article/<int:article_id>',article_detail,name="article_detail"),
```html
<!--直接点击能进入文章页面-->
<html>
<head>
</head>
<body>
    {% for article in articles %}
       <!--<p> <a href="/article/{{article.pk}}">{{article.title}}</a> </p>
       两个操作都可以
       -->
       <p> <a href="{%url 'article_detail' article.pk%}">{{article.title}}</a> </p>
    {% endfor %}
</body>
</html>


```
#####总urls包含app的urls
总路由 ` myite下 urls.py`
```python
from django.contrib import admin
from django.urls import include,path #增加了include
from .import views

urlpatterns = [
    # localhost:8000/  在主路由下的网址格式
    path('admin/', admin.site.urls),
    path('',views.index),
    path('article/',include('article.urls')),
    #包含分路由 网址格式为  localhost:8000/article/
]
```
分路由 ` article下 urls.py`
```python
from django.urls import path
from . import views #引用views文件
urlpatterns = [
    # localhost:8000/article/
    path('',views.article_list,name="article_list"),
    # localhost:8000/article/<int:article_id>
    path('<int:article_id>',views.article_detail,name="article_detail"),
]
```