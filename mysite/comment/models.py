from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 
from django.contrib.auth.models import User

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING) # models.CASCADE 删除阅读次数会删除博客   DO_NOTHING  删除阅读次数对应博客本身无影响
    object_id = models.PositiveIntegerField()  
    content_object = GenericForeignKey('content_type', 'object_id') # 评论对象

    text = models.TextField() # 评论内容
    comment_time = models.DateTimeField(auto_now_add=True) # 评论时间
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING) # 评论者

    class Meta: # 排序设置 倒叙
        ordering = ['-comment_time']