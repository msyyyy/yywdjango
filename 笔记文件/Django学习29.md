# 完善点赞功能

> 1. 新增评论和回复无法点赞

新增评论和回复没有onclick
字符串拼接问题
```js
 String.prototype.format = function(){ // 字符串拼接 '{0} + {1} + {0}'.format('a','b') 为 "a+b+c"
    var str = this;
    for (var i = 0;i < arguments.length; i++){
        var str = str.replace(new RegExp('\\{' + i + '\\}','g'), arguments[i]) // g 代表 全局
    };
    return str;
}

 var comment_html =
'<div id="root_{0}" class="comment">' +
    '<span>{1}</span>' +
    '<span>({2}):</span>' +
    '<div id="comment_{0}">{3}</div>' +
    '<div class="like" onclick="likeChange(this,\'{4}\',{0})">' +
        '<span class="glyphicon glyphicon-thumbs-up "></span> ' +
        '<span class="liked-num">0</span>' +
    '</div>' +
    '<a href="javascript:reply({0});">回复</a>' +
'</div>';

comment_html = comment_html.format(data['pk'],data['username'],timeFormat(data['comment_time']),data['text'],data['content_type']);

```
2. 未登录情况下点赞

弹出登录框
bootstrap 模态框
异步提交登录框

`mysite/views.py`增加点赞登录的方法

```python
def login_for_medal(request): # 按点赞时能登录
    login_form = LoginForm(request.POST)
    data = {}

    if login_form.is_valid(): 
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
```

`mysite/urls.py` 设置路由
```python
   path('login_for_medal/',views.login_for_medal, name='login_for_medal'), # 从点赞登录
```

`blog_detail.html`
```html
 <!--  登录 （bootstrap 模态框） -->
<div class="modal fade" id="login_modal" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-sm" role="document">
        <div class="modal-content">
            <form id="login_medal_form" action="" method="POST">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title">登录</h4>
                </div>

                <div class="modal-body">
                        {% csrf_token %}
                        {% for field in login_form %}
                            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                            {{ field }}
                        {% endfor %}
                        <span id="login_medal_tip" class="text-danger"></span>
                </div>

                <div class="modal-footer">
                    <button type="submit" class="btn btn-primary">登录</button>
                    <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
                </div>
            </form>
        </div>
    </div>
</div>
```
```js
$("#login_medal_form").submit(function(event){
            event.preventDefault(); // 阻止页面提交 即不会点提价后 页面消失
            $.ajax({
                url: '{% url "login_for_medal" %}',
                type: 'POST',
                data: $(this).serialize(),
                cache: false, 
                success:function(data){
                    if(data['status']=='SUCCESS'){ // 登录成功
                        window.location.reload(); //当前窗口重新加载 刷新
                    }else{
                        $('#login_medal_tip').text('用户名或密码不正确');
                    }
                }
            });
        });
```