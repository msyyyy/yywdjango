# 获取评论数和细节处理

自定义模板标签 
在app内创建templatetags包
创建py文件
load标签加载该文件

> 1. comment 内新建 templatetags 创建  `comment_tags.py`

```python
from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment

register = template.Library()

@register.simple_tag()
def get_comment_count(obj): # 数量统计
    content_type = ContentType.objects.get_for_model(obj) # 获得obj对应ContentType
    return Comment.objects.filter(content_type=content_type,object_id=obj.pk).count()
```

外部调用
`blog_detail.html`

```html
{% load comment_tags %} 先加载

<li>评论:({% get_comment_count blog %})</li>

```

> 细节处理 

1. ajax 返回的日期

时间戳 timestamp
`comment/views.py`
```python
 data['comment_time'] = comment.comment_time.timestamp() # 时间戳
```
`blog_detail.html`
```js
  function numFormat(num){ //控制格式 保证 3 输出为 03 
            return ('00' + num).substr(-2);
        }
        function timeFormat(timestamp){ // 获取时间 时间戳转换为时间
            var datetime = new Date(timestamp * 1000); // 得到时间 以ms为单位转换为s ×1000
            var year = datetime.getFullYear();
            var month = numFormat(datetime.getMonth()+1); //得到月份从0开始+1 
            var day = numFormat(datetime.getDate());
            var hour = numFormat(datetime.getHours());
            var minute = numFormat(datetime.getMinutes());
            var second = numFormat(datetime.getSeconds());
            return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
            
        }

    timeFormat(data['comment_time'])
```
2. css样式调整

3. 级联删除

DO_NOTHING  可能会对数据完整性产生影响
修改 models.DO_NOTHING 为 models.CASCADE
删除user后会删除关联的comment  
删除顶级评论 也会删除 相连回复

3. django-ckeditor
