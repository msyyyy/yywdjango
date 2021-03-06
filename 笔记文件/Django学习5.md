####admin后台
显示文章标题
> article 下 models.py文件
```python
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length = 30)
    content = models.TextField()
    
    def __str__(self): 
        return "<Article: %s>" % self.title
```
> 显示title和content  图片一
> article 下 admin.py文件
```python
from django.contrib import admin
from .models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title","content")

admin.site.register(Article,ArticleAdmin) #新增了ArticleAdmin
```
让文章按id排序
```python
class ArticleAdmin(admin.ModelAdmin): #显示title和content
    list_display = ("id","title","content")
    ordering =("id",)  #id正序排序
    ordering =("-id",)  #id倒序排序
```
装饰器
```python
from django.contrib import admin
from .models import Article

# Register your models here.
@admin.register(Article) #这个效果和最下面注释的效果一样
class ArticleAdmin(admin.ModelAdmin): #显示title和content
    list_display = ("id","title","content")
    ordering =("id",)

#admin.site.register(Article,ArticleAdmin) 
```
####修改模型
修改模型要更新数据库
python manage.py makemigrations  #创建数据库迁移文件
python manage.py migrate    #更新数据库
(需要设置默认值)
> 1.增加 created_time模型
```python
from django.db import models
from django.utils import timezone #新增头文件

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length = 30)
    content = models.TextField()
    created_time =models.DateTimeField(default=timezone.now) #设置默认值为当前时间
    #也可以 created_time =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "<Article: %s>" % self.title
```
> 2.在admin中也增加created_time 显示
> 3.python manage.py makemigrations  #创建数据库迁移文件
运行后 数据库migrations文件夹中增加0002_article_created_time文件
```python
# Generated by Django 2.1.3 on 2018-12-01 06:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
```
> 4.python manage.py migrate    #更新数据库
总mysite下 db.sqlite3文件更新

增加最后发布时间
last_update_time = models.DateTimeField(auto_now=True)

如果有作者模型 我们要用到他的名字 我们要和他关联 外键
```python
 author = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=1) 
  #外键（关联到的模型,是否更改作者的信息（否）,默认值）
```
> 删除文章，如果我们要删除文章不是真的删除而是把他is_deleted属性改为True
is_deleted = models.BooleanField(default=False) #该文件是否被删除，默认否

> 删除文章不显示

`article 下 views.py文件`
```python
def article_list(request):
    articles = Article.objects.filter(is_deleted=False)#筛选出未被标记为删除的文章
    context = {}
    context['articles']=articles
    return render_to_response("article_list.html",context)
```


readed_num = models.IntegerField(default=0) #阅读数量