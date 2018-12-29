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
