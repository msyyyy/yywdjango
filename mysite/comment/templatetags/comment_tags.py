from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()

@register.simple_tag
def get_comment_count(obj): # 数量统计
    content_type = ContentType.objects.get_for_model(obj) # 获得obj对应ContentType
    return Comment.objects.filter(content_type=content_type,object_id=obj.pk).count()

@register.simple_tag
def get_comment_form(obj): # 获取评论表单
    content_type = ContentType.objects.get_for_model(obj) # 获得obj对应ContentType
    form  = CommentForm(initial={
        'content_type':content_type.model,
        'object_id': obj.pk,
        'reply_comment_id': 0})#  提交评论 传入字典给评论的content_type和object_id赋初值
    return form

@register.simple_tag
def get_comment_list(obj): # 获取具体一篇博客的评论列表
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type,object_id=obj.pk,parent=None) # 获取对应该博客的评论，获得一级评论
    return comments.order_by('-comment_time') # 倒叙排序
