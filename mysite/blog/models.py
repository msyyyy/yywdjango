from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail

class BlogType (models.Model):
    type_name = models.CharField(max_length=15)

    def __str__ (self):  #让文章选择分类时能看到分类名
        return self.type_name
    def blog_count(self): 
        return self.blog_set.count()  # blog_set 反向获取被关联外键的model（模型名称小写加_set）

class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE) # 删除博客对博客类型无影响  多对一
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail) # 反向关联到ReadDetail    关联以后直接 blog.read_details.all()就能查看该博客所有readdetail
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']  # 按时间排序  最新的在最前
