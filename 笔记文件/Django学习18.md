# 博客阅读计数

> 方法一  blog模型添加数字字段记录   每次有人打开次数+1 
`models.py`
```python
class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    read_num = models.IntegerField(default=0) # 阅读次数
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title


    class Meta:
        ordering = ['-created_time']
```
`admin.py`
```python
@admin.register(Blog)
class BlogAdmain(admin.ModelAdmin):
    list_display = ('title','blog_type','author','read_num','created_time','last_updated_time')
```
`views.py`
```python
def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog,pk=blog_pk)
    blog.read_num +=1    # 阅读数+1 
    blog.save()          # 保存下来
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() # 获取上一篇博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 获取下一篇博客 
    context['blog'] = blog
    return render_to_response('blog/blog_detail.html',context)
```

## 自定义计数规则 
因为之前刷新一次就计数+1 有点多
同一个人   隔一定时间以后才又算一次 
传出cookie 
###  `views.py`
```python
def blog_detail(request,blog_pk):
    context = {}
    blog = get_object_or_404(Blog,pk=blog_pk)
    if not request.COOKIES.get('blog_%s_read' % blog_pk): # 如果不存在这个cookie ，增加阅读次数
        blog.read_num +=1
        blog.save()
        
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() # 获取上一篇博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 获取下一篇博客 
    context['blog'] = blog
    response = render_to_response('blog/blog_detail.html',context) # 响应
    response.set_cookie('blog_%s_read' % blog_pk,'true' ) # 键值  权值   max_age有效期持续时间   expires 有效期到多久为止,
    #有了expires 则 max_age 无效 如果两个都不设置  那么打开浏览器时一直有效 关闭浏览器失效 
    return response

```

## 该方法缺点

1. 后台编辑博客可能影响数据  每次有人阅读会修改博客最后改动时间  其实我们是不想改的

2. 功能单一  无法统计某一天的阅读数