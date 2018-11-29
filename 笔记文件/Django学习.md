
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

```
from .models import Article  先从models把Aeticle 类引用


admin.site.register(Article) 
```