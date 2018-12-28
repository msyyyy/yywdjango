from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 
from django.contrib.auth.models import User

class Comment(models.Model): # 评论
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # models.CASCADE 删除博客会删除阅读数 
    object_id = models.PositiveIntegerField()  
    content_object = GenericForeignKey('content_type', 'object_id') # 评论对象

    text = models.TextField() # 评论内容
    comment_time = models.DateTimeField(auto_now_add=True) # 评论时间
    user = models.ForeignKey(User, related_name="comments",on_delete=models.CASCADE) # 评论者
    # 这条评论是基于哪一条评论开始的 
    root = models.ForeignKey('self', related_name="root_comment",null=True,on_delete=models.CASCADE)
    # 他的评论对象级数 指向自己  允许为空(为空就是指向博客)
    parent = models.ForeignKey('self',related_name="parent_comment",null=True,on_delete=models.CASCADE)
    # 回复谁,评论对象
    reply_to = models.ForeignKey(User, related_name="replies",null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    class Meta: # 排序设置 正序
        ordering = ['comment_time']

