# 分页和shell命令行模式

文章过多 需要分页加载

> shell 下命令
```
from blog.models import Blog   添加class
dir() 查看当前下的class


dir( 实例 )  查看当前实例的方法

blog = Blog()  创建新的实例

blog.title = "shell下第一篇"
blog.content = "sadasda"

from blog.models import BlogType
blog_type  = BlogType.objects.all()[0]
要创建新博客时 如果blog模型用到了外键我们得把这个外键引用进来
blog.blog_type =blog_type

from django.contrib.auth.models import User
user = User.objects.all()[0]
blog.author = user

除了有默认值的属性以外全部填写完毕 
blog.save()  保存


Blog.objects.all()  查看所有blog
BlogType.objects.all().count()  查看blog数目
del Blog  移除 Blog类


 for i in range(1,31):     for循环文章创建
     blog = Blog()
     blog.title = "for %s " % i
     blog.content = "xxxxxx:%s" % i
     blog.author = user
     blog.blog_type = blog_type
     blog.save()
```
> 分页器
```

以下操作在shell中   ，不过只是看一下

from django.core.paginator import Paginator     # 引入

先得让blog排序  我们这边就让blog由时间倒叙

class Blog(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']   倒叙

然后我们得跟新同步数据库

paginator = Paginator(blogs,10)  分成每10篇博客每页

dir( paginator ) 看这个有什么方法

比如 paginator.num_pages 查看页数

```
GET请求 如 通过 http://localhost:8000/blog/？page=1 访问

## `view.py`
```python
def blog_list(request):

    blogs_all_list=Blog.objects.all()
    paginator = Paginator(blogs_all_list,10) #每10页进行分页
    page_num = request.GET.get('page',1) #获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num) #如果得到的是非法页码自动返回 1

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs  #传入分页信息
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html',context)
```
## `blog_list.html`
```html
<div>
    <ul class="pagination">
        {# 上一页码 #}
        <li>
            {% if page_of_blogs.has_previous %}  {# 判断是否有上一页 #}
                <a href="?page={{ page_of_blogs.previous_page_number }}"  aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            {% else %}
                <span aria-hidden="true">&laquo;</span>
            {% endif %}
        
        </li>
        {# 全部页码 #}
        {% for page_num in page_of_blogs.paginator.page_range %} 
            <li><a href="?page={{ page_num }}">{{ page_num }}</a></li>
        {% endfor %}    

        {# 下一页码 #}
        <li>
            {% if page_of_blogs.has_next %} 
                <a href="?page={{ page_of_blogs.next_page_number }}" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            {% else %}
                <span aria-hidden="true">&raquo;</span>
            {% endif %}
        
        </li>
    </ul>
</div>
```