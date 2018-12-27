# 回复功能 和 树结构

评论可被回复  回复可被回复

> 创建 评论对象级数和评论对象的外键

为了解决两个相同外键冲突问题 增加 related_name
```python
 user = models.ForeignKey(User, related_name="comments",on_delete=models.DO_NOTHING) # 评论者
# 他的评论对象级数 指向自己  允许为空(为空就是指向博客)
 parent = models.ForeignKey('self',null=True,on_delete=models.DO_NOTHING)
# 回复谁,评论对象
reply_to = models.ForeignKey(User, related_name="replies",null=True,on_delete=models.DO_NOTHING)

```
> 显示下一级的评论

```html

<!--将他下一级的评论取出 回复他的评论-->
{% for reply in comment.root_comment.all %} 
    <div class="reply">
        {{ reply.user.username }}
        ({{ reply.comment_time|date:"Y-m-d H:i:s" }}):
        回复
        {{ reply.reply_to.username }}
        {{ reply.text|safe }}
    </div>
{% endfor %}
```

> 创建回复按钮 回复时在编辑框上面显示要回复的内容 
`blog_detail.html`
```html
<div id="reply_content_container" style="display:none;">
    <p>回复: </p>
    <div id="reply_content"></div>
</div>


<div class="comment-area">
    <h3 class="comment-area-title">评论列表</h3>
    <div id="comment_list">
        {% for comment in comments %}
            <div class="comment">
                {{ comment.user.username }}
                ({{ comment.comment_time|date:"Y-m-d H:i:s" }}):
                
                <div id="comment_{{ comment.pk }}">
                    {{ comment.text|safe }}
                </div>
                <!--调用下面script中reply 方法 传入的是该条评论的id值 -->
                <a href="javascript:reply({{ comment.pk }});">回复</a> 
                
                <!--将他下一级的评论取出 回复他的评论-->
                {% for reply in comment.root_comment.all %} 
                    <div class="reply">
                        {{ reply.user.username }}
                        ({{ reply.comment_time|date:"Y-m-d H:i:s" }}):
                        回复
                        {{ reply.reply_to.username }}
                        <div id="comment_{{ reply.pk }}">
                                {{ reply.text|safe }}
                            </div>
                        <a href="javascript:reply({{ reply.pk }});">回复</a>
                    </div>
                {% endfor %}
            </div>
        {% empty %}
            <span id="no_comment">暂无评论</span>
        {% endfor %}
    </div>      
</div>

{% block script_extends %}
    <script type="text/javascript"> 
        $("#comment_form").submit(function(){ //选择出了id 为comment_form 的标签
            $("#comment_error").text(''); //清掉错误提示
            // 判断是否为空 若为空则不提交 trim把取到的内容换行和空格都忽略
            if (CKEDITOR.instances["id_text"].document.getBody().getText().trim()==''){
                $("#comment_error").text('评论内容不能为空');
                return false;
            }
            // 跟新数据到textarea
            CKEDITOR.instances['id_text'].updateElement();

            // 异步提交
            $.ajax({ //是一个字典
                url: "{% url 'update_comment' %}" ,//向那个链接提交数据
                type: 'POST', //提交类型
                data: $(this).serialize(), // 获取评论内容 this 即当前comment_form
                cache: false, //不需要缓存
                success: function(data){ // 如果提交成功返回data
                    console.log(data); //显示出来
                    if(data['status']=="SUCCESS"){
                        // 插入数据
                        var comment_html = '<div>' + data['username'] +
                                            '(' + data['comment_time'] + '): ' +
                                            data['text'] + '</div>';
                        $("#comment_list").prepend(comment_html);
                        // 清空编辑框内容
                        CKEDITOR.instances['id_text'].setData('')
                        $("no_comment").remove() // 去掉暂无评论
                    }else{
                        // 显示错误信息
                        $("#comment_error").text(data['message']);
                    }
                },
                error: function(xhr){
                    console.log(xhr);
                }
            });
            return false;
        })
        function reply(reply_comment_id){
            //设置值
            $('reply_comment_id').val(reply_comment_id); //修改reply_comment_id的值
            var html =$("#comment_" + reply_comment_id).html(); // 选择器 得到html
            $('#reply_content').html(html); 
            $('#reply_content_container').show(); //在上面显示出要回复对象的内容
            
            // 页面回滚到提交评论那边
            $('html').animate({scrollTop:$('#comment_form').offset().top - 60 },300,function(){
                CKEDITOR.instances['id_text'].focus();

            }); 
            
        }
    </script>

{% endblock %}


```

> 保存数据 
 
`forms.py`
```python
  # 回复的对象 0 代表初始值说明他是评论文章 否则回复评论
    def clean_reply_comment_id(self): 
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = blank=True, null=True
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        return reply_comment_id
         
```

`comment/views.py`
```python
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse # 反向通过别名得到网址
from django.http import JsonResponse 
from .models import Comment
from .forms import CommentForm

def update_comment(request): # 提交评论

    referer =  request.META.get('HTTP_REFERER', reverse('home')) # 获取是从哪个网址跳转过来的 如果获取不到 那么返回首页(通过别名反向得到链接)
    comment_form = CommentForm(request.POST,user=request.user) # 实例化 把user传到CommentForm
    data = {}
    if comment_form.is_valid():
        # 检查已通过,保存数据
        comment = Comment() # 实例化一条评论
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None: # 这说明他评论的不是文章而是评论
            comment.root = parent.root if not parent.root is None else parent # 顶级评论的root也为None,如果他评论对象是顶级评论 那么root是他的评论对象 否则root为顶级对象
            comment.parent = parent 
            comment.reply_to = parent.user
        comment.save()
        
        # 返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S') # 字符串化时间
        data['text'] = comment.text
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
    else:
        # return render(request, 'error.html',{'message':comment_form.errors,'redirect_to': referer })
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)

```

`blog_detail.html`
```html
function reply(reply_comment_id){
    //设置值
    $('#reply_comment_id').val(reply_comment_id); //修改reply_comment_id的值
    var html =$("#comment_" + reply_comment_id).html(); // 选择器 得到html 然后获得其文章内容
    $('#reply_content').html(html);
    $('#reply_content_container').show(); //在上面显示出要回复对象的内容

    // 页面回滚到提交评论那边
    $('html').animate({scrollTop:$('#comment_form').offset().top - 60 },300,function(){
        CKEDITOR.instances['id_text'].focus();

    }); 
    
}
```