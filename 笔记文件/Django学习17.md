# 博客后台富文本编辑

简单文本编辑  ----> 直接贴入html 代码

富文本 ----> 最终解析成html   比如    富文本编辑器     markdown编辑器

<div class="blog-content">{{ blog.content|safe }}</div>  让直接写入的html代码有效

<p>{{ blog.content|striptags|truncatechars:60}}</p>  去掉html代码 保留原内容 然后再取前60个字符

## 选择了 django-ckeditor 

> 1. 安装 pip install django-ckeditor

> 2. 注册  在 `settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'ckeditor',
]
```
> 3. 配置model  把字段改成RichTextField

`models.py`
```python
from ckeditor.fields import RichTextField
class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = RichTextField()  #富文本编辑
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title


    class Meta:
        ordering = ['-created_time']
```
> 4. 数据库迁移

## 配置完成后 发现没有上传图片的功能

> 1. 安装 pip install pillow     #图片库管理 

> 2. 注册应用 'ckeditor_uploader'
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'ckeditor',
    'ckeditor_uploader',
]
```
> 3. 配置settings  然后在住myiste文件中创建medio文件夹
`settings.py`
```python
# media 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# 配置ckeditor
CKEDITOR_UPLOAD_PATH='upload/'
```
> 4. 配置 url    总`urls.py`
```python
from django.contrib import admin
from django.urls import include,path   # 新增
from django.conf import settings   # 新增
from django.conf.urls.static import static
from . import  views

urlpatterns = [
    path('',views.home,name='home'),
    path('admin/', admin.site.urls),
    path('ckeditor',include('ckeditor_uploader.urls')), # 新增
    path('blog/',include('blog.urls')),

]

urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)   # 新增
```
> 5. 配置model  把字段改成 RichTextUploadingField
```python
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField # 改变

class BlogType (models.Model):
    type_name = models.CharField(max_length=15)

    def __str__ (self):  #让文章选择分类时能看到分类名
        return self.type_name
    def blog_count(self): 
        return self.blog_set.count()  # blog_set 反向获取被关联外键的model（模型名称小写加_set）

class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()      # 改变
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title


    class Meta:
        ordering = ['-created_time']
```
> 6. 数据库迁移