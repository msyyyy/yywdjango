### 初步建立blog应用
建立博客属性和博客分类 两个类
> 1. blog下models文件修改 模型
```python
from django.db import models
from django.contrib.auth.models import User 

class BlogType (models.Model):
    type_name = models.CharField(max_length=15)

    def __str__ (self): #让文章选择分类时能看到分类名
        return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

```


> 2.  blog下admin文件修改
```python
from django.contrib import admin
from .models import BlogType,Blog

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin): #在进入文章类型管理时能看到文章类型的id和type_name
    list_display = ('id','type_name')

@admin.register(Blog)
class BlogAdmain(admin.ModelAdmin):
    list_display = ('title','blog_type','author','created_time','last_updated_time')
```




#### pip一键导出和安装
> pip freeze 查看安装了那些库

> pip freeze > requirements.txt
将信息导出到该txt文件

> pip install -r requirements.txt
一键安装


