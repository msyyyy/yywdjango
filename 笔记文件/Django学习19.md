# 博客阅读计数优化

计数功能独立

## 外键
```python
比如 博客 外键 博客类型
    阅读数 外键  博客
blog_type.blog_set.all() # 得到所有这个博客类型的博客

blog.readnum  # 得到的是ReadNum类型的实例

blog.readnum.read_num # 得到阅读数
```
> 方法一 新建模型
## `models.py`
```python
class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING) # 删除博客对博客类型无影响  多对一
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def get_read_num(self):   # 新增得到阅读数的方法
        return self.readnum.read_num  # 一对一才有 .readnum

    def __str__(self):
        return "<Blog: %s>" % self.title


    class Meta:
        ordering = ['-created_time']  # 按时间排序  最新的在最前

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0) # 阅读次数
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING) # 删除阅读数据对博客本身无影响   一对一

```
## `views.py`
```python
def blog_detail(request,blog_pk):
    
    blog = get_object_or_404(Blog,pk=blog_pk)
    if not request.COOKIES.get('blog_%s_read' % blog_pk): # 还没阅读过这篇博客
        if ReadNum.objects.filter(blog=blog).count():  # 检测这篇博客的阅读数记录是否存在
            # 存在
            readnum = ReadNum.objects.get(blog=blog) # 挑选出这条记录
        else:
            # 不存在对应记录
            readnum = ReadNum(blog=blog)  # 实例化
        # 计数加1   
        readnum.read_num += 1 
        readnum.save()  # 保存 

    context = {}    
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() # 获取上一篇博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 获取下一篇博客 
    context['blog'] = blog
    response = render_to_response('blog/blog_detail.html',context) # 响应
    response.set_cookie('blog_%s_read' % blog_pk,'true' ) # 键值  权值   max_age有效期持续时间   expires 有效期到多久为止,
    #有了expires 则 max_age 无效 如果两个都不设置  那么打开浏览器时一直有效 关闭浏览器失效 
    return response

```
## `admin.py`
```python
from django.contrib import admin
from .models import BlogType,Blog ,ReadNum

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

@admin.register(Blog)
class BlogAdmain(admin.ModelAdmin):
    list_display = ('title','blog_type','author','get_read_num','created_time','last_updated_time')

@admin.register(ReadNum)
class ReadNumAdmain(admin.ModelAdmin):
    list_display = ('read_num','blog')
```

> 一开始他不自己显示0 可能没有对应的阅读记录
`models.py`
```python
def get_read_num(self):   # 新增得到阅读数的方法
    try:                 # 会先完成try中的代码 如果完成中发生获取不到的错误 执行后一条
        return self.readnum.read_num  # 一对一才有 .readnum
    except exceptions.ObjectDoesNotExist:  # except Exception as e  不管什么错误都会获取    
        return 0;                          #   exceptions.ObjectDoesNotExist  记录不存在的错误返回 0
            
```

> 方法二 可以对任何模型计数  内置模型 ContentTypes （更优）

### 1. 创建新的app   python3 manage.py startapp read_statistics  更新数据库

`read_statistics/models.py`
```python
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey 
from django.contrib.contenttypes.models import ContentType

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0) # 阅读次数
    
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING) #models.CASCADE 删除阅读次数会删除博客   DO_NOTHING  删除阅读次数对应博客本身无影响
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
```

` read_statistics/admin.py`
```python
from django.contrib import admin
from .models import ReadNum

@admin.register(ReadNum)
class ReadNumAdmain(admin.ModelAdmin):
    list_display = ('read_num','content_object')
```


`shell模式下`
```
 ct = ContentType.objects.get_for_model(Blog) # 获取关联到Blog的 ContentType 实例
 blog = Blog.objects.first()
 rn = ReadNum.objects.filter(content_type = ct ,object_id = blog.pk)[0]  # 获得所有关联到Blog ， id值= blog.pk 这个blog的 ReadNum ，然后取出第一个
 rn.read_num    # 查看这一条记录的阅读次数


 filter 是选出所有包含条件的 如果没有获得 []
 get 是选出一个满足条件的  如果没有或者 有两个以上会报错
```

### 2. 完成添加app到settings 后 
修改 `blog/models.py`
```python
class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING) # 删除博客对博客类型无影响  多对一
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    
    def get_read_num(self):   # 新增得到阅读数的方法
        try:                 # 会先完成try中的代码 如果完成中发生获取不到的错误 执行后一条
            ct = ContentType.objects.get_for_model(Blog) # 获取关联到Blog的 ContentType 实例 这里的Blog改self也行
            readnum = ReadNum.objects.get(content_type = ct ,object_id = self.pk)  # 获得所有关联到Blog ， id值= self.pk 这个blog的 ReadNum 
            return readnum.read_num    # 查看这一条记录的阅读次数
        except exceptions.ObjectDoesNotExist:  # except Exception as e  不管什么错误都会获取    
            return 0;                          # exceptions.ObjectDoesNotExist  记录不存在的错误返回 0

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']  # 按时间排序  最新的在最前

```
修改`blog/views.py` 
```python
def blog_detail(request,blog_pk):
    
    blog = get_object_or_404(Blog,pk=blog_pk)
    
    if not request.COOKIES.get('blog_%s_read' % blog_pk): # 还没阅读过这篇博客
        ct = ContentType.objects.get_for_model(Blog)  
        if ReadNum.objects.filter(content_type = ct ,object_id = blog.pk).count():  # 检测这篇博客的阅读数记录是否存在 
            # 存在
            readnum = ReadNum.objects.get(content_type = ct ,object_id = blog.pk) # 挑选出这条记录
        else:
            # 不存在对应记录
            readnum = ReadNum(content_type = ct ,object_id = blog.pk)  # 实例化
        # 计数加1   
        readnum.read_num += 1 
        readnum.save()  # 保存
```
完成了计数的优化


## 类的封装和继承

>  封装阅读次数类

以后不仅blog能用 所有要用到阅读数这个类的都能用

### `read_statistics/models.py`
```python
from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0) # 阅读次数

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING) # models.CASCADE 删除阅读次数会删除博客   DO_NOTHING  删除阅读次数对应博客本身无影响
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpandMethod():   # 封装了一个类 以后要用到下面的方法继承这个类就行
    def get_read_num(self):   # 新增得到阅读数的方法
        try:                 # 会先完成try中的代码 如果完成中发生获取不到的错误 执行后一条
            ct = ContentType.objects.get_for_model(self) # 获取关联到Blog的 ContentType 实例
            readnum = ReadNum.objects.get(content_type = ct ,object_id = self.pk)  # 获得所有关联到Blog ， id值= self.pk 这个blog的 ReadNum 
            return readnum.read_num    # 查看这一条记录的阅读次数
        except exceptions.ObjectDoesNotExist:  # except Exception as e  不管什么错误都会获取    
            return 0                        # exceptions.ObjectDoesNotExist  记录不存在的错误返回 0
```

### `blog/models.py`

```python
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod

class BlogType (models.Model):
    type_name = models.CharField(max_length=15)

    def __str__ (self):  #让文章选择分类时能看到分类名
        return self.type_name
    def blog_count(self): 
        return self.blog_set.count()  # blog_set 反向获取被关联外键的model（模型名称小写加_set）

class Blog(models.Model,ReadNumExpandMethod):  # 继承类
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING) # 删除博客对博客类型无影响  多对一
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']  # 按时间排序  最新的在最前

```

> 封装 每次点击会增加阅读量的方法

### 在 read_statistics 新建 `utils.py`

以后不仅blog能用 所有要用到增加阅读数这个方法的都能用

```python
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum

def read_statistics_once_read(request, obj): # 这里传 obj是为了告诉ContentType 传进来的与Blog还是其他什么对应
    ct = ContentType.objects.get_for_model(obj)
    key ="%s_%s_read" % (ct.model, obj.pk)   # 对应应该有的cookie值

    if not request.COOKIES.get(key): # 还没阅读过
        if ReadNum.objects.filter(content_type = ct ,object_id = obj.pk).count():  # 检测这个阅读数记录是否存在 
            # 存在
            readnum = ReadNum.objects.get(content_type = ct ,object_id = obj.pk) # 挑选出这条记录
        else:
            # 不存在对应记录
            readnum = ReadNum(content_type = ct ,object_id = obj.pk)  # 实例化
        # 计数加1   
        readnum.read_num += 1 
        readnum.save()  # 保存
    return key   # 最后返回的是一个cookie标记
```

### 修稿 `blog/views.py`

```python
from read_statistics.utils import read_statistics_once_read

def blog_detail(request,blog_pk):
    
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog) 
     
    context = {}    
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() # 获取上一篇博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 获取下一篇博客 
    context['blog'] = blog
    response = render_to_response('blog/blog_detail.html',context) # 响应
    response.set_cookie(read_cookie_key,'true' ) # 键值  权值   max_age有效期持续时间   expires 有效期到多久为止,
    #有了expires 则 max_age 无效 如果两个都不设置  那么打开浏览器时一直有效 关闭浏览器失效 
    return response

```