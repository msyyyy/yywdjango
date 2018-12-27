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

2. css样式调整

3. 级联删除

3. django-ckeditor
