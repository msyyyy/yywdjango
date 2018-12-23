# 富文本编辑和ajax提交评论

django-ckeditor 富文本表单
每个字段类型有一个适当的默认 Widget类
from ckeditor.widgets import CKEditorWidget

> 1. 创建`comment/forms.py`新建CommentForm模型

```python
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist 

class CommentForm(forms.Form):
    # widget=forms.HiddenInput 隐藏不显示
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput) 
    # Textarea 能输入多行字符
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs): # 之前实例化过程中上传了一个user，这边接收 
        if 'user' in kwargs: # 存在user
            self.user = kwargs.pop('user') # 取出并抛弃
        super(CommentForm,self).__init__( *args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if  self.user.is_authenticated: # 因为前端页面不是绝对可靠的,所有再次判断  
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
            
        # 评论对象验证 评论对象不存在不能评论
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model=content_type).model_class() # 得到该文章类型的具体模型 比如这里model_class 可能为Blog
            model_obj = model_class.objects.get(pk=object_id)   # 找到具体哪一篇文章
            self.cleaned_data['content_object'] = model_obj  # 保存这个content_object属性 方便以后访问
        except ObjectDoesNotExist: # 只有当get不到文章时会报这个错
            raise forms.ValidationError('评论对象不存在')
        
        return self.cleaned_data
```

> 2. 传输个前段模板页面 `blog/views.py` ，前段模板页面显示  `blog_detaiil.html`

> 3. `comment/view.py` 创建提交评论的方法

```python
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse # 反向通过别名得到网址
from .models import Comment
from .forms import CommentForm

def update_comment(request): # 提交评论

    referer =  request.META.get('HTTP_REFERER', reverse('home')) # 获取是从哪个网址跳转过来的 如果获取不到 那么返回首页(通过别名反向得到链接)
    comment_form = CommentForm(request.POST,user=request.user) # 实例化 把user传到CommentForm
    
    if comment_form.is_valid():
        # 检查已通过,保存数据
        comment = Comment() # 实例化一条评论
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        return redirect(referer)
    else:
        return render(request, 'error.html',{'message':comment_form.errors,'redirect_to': referer })
```

## 但是现在只是做到了通过form代替之前的代码  还没有做到富文本编辑

`froms.py`

from ckeditor.widgets import CKEditorWidget

`blog_detail.html`

<script type="text/javascript" src="{% static "ckeditor/ckeditor-init.js" %}"></script>
<script type="text/javascript" src="{% static "ckeditor/ckeditor/ckeditor.js" %}"></script>

## 添加了富文本 ，自定义
text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor')) 
在 setting.py中自定义

# ajax提交 

正常提交会刷新页面 ajax提交是一种不刷新页面的异步提交方式

> 1. 提交数据

`blog_deatil.html`
```html
{% block script_extends %}
    <script type="text/javascript"> 
        $("#comment_form").submit(function(){ //选择出了id 为comment_form 的标签
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
                },
                error: function(xhr){
                    console.log(xhr);
                }
            });
            return false;
        })
    </script>
{% endblock %}
```

> 2. 返回数据

`comment/views.py` 传回去数据
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
        comment.save()
        
        # 返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S') # 字符串化时间
        data['text'] = comment.text
    else:
        # return render(request, 'error.html',{'message':comment_form.errors,'redirect_to': referer })
        data['status'] = 'ERROR'
    return JsonResponse(data)
```

`blog_detail.html`
```html
<h3 class="comment-area-title">提交评论</h3>
{% if user.is_authenticated %}
    <form id= "comment_form" action="{% url 'update_comment' %}" method="POST" style="overflow:hidden"> <!--发布评论 发送给提交页面-->
        <label>{{ user.username }} 欢迎评论~~</label>
        {% csrf_token %} 
        {% for field in comment_form %}
            {{ field }}
        {% endfor %}
        <input type="submit" value="评论" class="btn btn-primary" style="float:right">
    </form>
{% else %}
    您尚未未登录,登录之后方可评论~
    <a class="btn btn-primary" href="{% url 'login' %}?from={{ request.get_full_path }}">登录</a> <!--?from={{ request.get_full_path }}把从哪里来的链接发送进去登录以后可以跳转回来-->
    <span>or</span>
    <a class="btn btn-danger" href="{% url 'register' %}?from={{ request.get_full_path }}">注册</a> 
{% endif %}

{% block script_extends %}
    <script type="text/javascript"> 
        $("#comment_form").submit(function(){ //选择出了id 为comment_form 的标签
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
                    }else{

                    }
                },
                error: function(xhr){
                    console.log(xhr);
                }
            });
            return false;
        })
    </script>
{% endblock %}

```
## 时间不对的话可以去 setting改一下时区

TIME_ZONE = 'Asia/Shanghai'

## 点击提交后情况评论框 

CKEDITOR.instances['id_text'].setData('')

## 提交后去掉暂无评论

<span id="no_comment">暂无评论</span>

提交成功后
$("no_comment").remove() // 去掉暂无评论