from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount,LikeRecord

register = template.Library()

@register.simple_tag
def get_like_count(obj): # 获取点赞数量
    content_type = ContentType.objects.get_for_model(obj) # 获得obj对应ContentType
    like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=obj.pk)
    return like_count.liked_num

@register.simple_tag(takes_context=True) # 能够使用当前模板页面使用的模板变量 就能得到user了
def get_like_status(context,obj): # 是否点赞
    content_type = ContentType.objects.get_for_model(obj)
    user=context['user'] # 获取到当前模板页面的user
    if not user.is_authenticated:  # 如果还没有登录
        return ''
    if LikeRecord.objects.filter(content_type=content_type,object_id=obj.pk,user=user).exists(): # 如果点赞记录已存在
        return 'active'
    else:
        return ''

@register.simple_tag
def get_content_type(obj): # 获取相应的ContentType类型
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model 