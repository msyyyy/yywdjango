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

> 3. 调用方法写入 `views.py`
```python
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated: # 未登录
        return ErrorResponse(400,'you were not login')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id) # 是否有该篇博客
    except ObjectDoesNotExist:  # 如果捕捉到不存在的错误
        return ErrorResponse(401,'object not exist')


    # 处理数据
    if request.GET.get('is_like') == 'true': # 要点赞
        # 查找或创建点赞数据 如果是创建 created 为 true
        like_record,created = LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
        if created: # 未点赞过，要点赞
            # 查找或创建该文章点赞总数
            like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else: # 已经点赞过 ，不能重复点赞
            return ErrorResponse(402,'you were liked')

    else:# 要取消点赞
        if LikeRecord.objects.filter(content_type=content_type,object_id=object_id,user=user).exists():
            # 有点赞过 取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type,object_id=object_id,user=user)
            like_record.delete() # 删除点赞数据
            # 点赞总数减一
            like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            if not created: # 如果不是新创建的数据 即数据正常
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404,'data error')

        else: # 未点赞过
            return ErrorResponse(403,'you were not liked')
    
```

> 3. 显示点赞数 创建templatetags文件夹 在其中创建 `liked_tags.py`

```python
from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount

register = template.Library()

@register.simple_tag
def get_like_count(obj): # 获取点赞数量
    content_type = ContentType.objects.get_for_model(obj) # 获得obj对应ContentType
    like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=obj.pk)
    return like_count.liked_num

```

> 4. 在`blog_detail.html` 和`bolg_list.html`  显示出来
```html
{% load likes_tags %} 引入

{% get_like_count blog %} 显示
```

> 5.  点赞与取消点赞的js实现 增加与删除 active 标签

```js
 function likeChange(obj, content_type, object_id){ //点赞或取消点赞
            var is_like = obj.getElementsByClassName('active').length == 0 // 获取是否已经点赞 已经点赞会有active标签
            $.ajax({ //发送请求
                url: "{% url 'like_change' %}", // q向哪里发送
                type: 'GET', // 发送的种类
                data: {  //发送内容
                        content_type: content_type,
                        object_id: object_id ,
                        is_like: is_like
                },
                cache: false, //是否有缓存
                success: function(data){ //请求成功
                    console.log(data)
                    if(data['status']=='SUCCESS'){ // 请求成功
                        // 跟新点赞状态
                        var element = $(obj.getElementsByClassName('glyphicon')); // 获取glyphicon这一层
                        if(is_like){ // 如果是要点赞
                            element.addClass('active'); // 给这层 加上 active 标签 
                        }else{ // 要取消点赞
                            element.removeClass('active'); // 移除 active 标签 
                        }
                        // 跟新点赞数量
                        var liked_num = $(obj.getElementsByClassName('liked-num'));
                        liked_num.text(data['liked_num']); // 跟新点赞数

                    }else{
                        alert(data['message']);//弹窗 错误信息
                    }
                },
                error: function(xhr){ //发生错误
                    console.log(xhr)
                }
            });
        }
```

> 6. 应用到评论 回复 点赞


# 功能需求分析 - 模型设计 - 前段初步开发 - 后端实现 - 完善前段代码