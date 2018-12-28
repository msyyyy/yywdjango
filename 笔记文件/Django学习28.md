# 点赞功能设计

1. 博客和评论 回复都能点赞

2. 可以取消点赞

3. 可以看到点赞总数

前后端交替进行  可以先写前段需求


> 1. 创建app likes   创建模型   注册app
`likes/models.py`
```python
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 
from django.contrib.auth.models import User

class LikeCount(models.Model):  # 点赞数量
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) 
    object_id = models.PositiveIntegerField()  
    content_object = GenericForeignKey('content_type', 'object_id') # 点赞对象

    liked_num = models.IntegerField(default=0) # 点赞数量

class LikeRecord(models.Model): # 具体点赞数据
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) 
    object_id = models.PositiveIntegerField()  
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User ,on_delete=models.CASCADE) # 点赞者
    liked_time = models.DateTimeField(auto_now_add=True) 


```
> 2.  前段模板页面写入

增加图标
``` html
<div class="like" onclick=""> <!-- onlick 为点击操作 点击后触发-->
    <span class="glyphicon glyphicon-thumbs-up"></span>
    <span class="liked-num">0</span>
    <span>喜欢</span>
</div>

```
```js
function likeChange(){ //点赞或取消点赞
    $ajax({ //发送请求
        url: '?', // q向哪里发送
        type: 'GET', // 发送的种类
        data: {  //发送内容

        },
        cache: false, //是否有缓存
        success: function(data){ //请求成功

        },
        error: function(xhr){ //发生错误

        }
    });
}
```
如果被点赞那么修改图标颜色
```css
div.like {   /* 点赞图标 */
    color: #337ab7;
    cursor: pointer;  /* 可以点击 */
    display: inline-block;
    padding: 0.5em 0.3em; /* 上下0.5em 左右0.3em */
}
div.like .active { /* 点赞图标被点击后 */
    color: #f22;
}
```

> 2. 创建urls  ,总路由包括分路由
```python
from django.urls import path
from . import  views

urlpatterns = [
    path('like_change',views.like_change,name='like_change'), # 改变是否点赞
]

```