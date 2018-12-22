# 富文本编辑和ajax提交评论

django-ckeditor 富文本表单
每个字段类型有一个适当的默认 Widget类
from ckeditor.widgets import CKEditorWidget

> 1. 创建`comment/forms.py`

```python
from django import forms

class CommentForm(forms.Form):
    content_type = forms.CharField()
    object_id = forms.IntegerField()
    text = forms.CharField()
```

> 2. 传输个前段模板页面  ，前段模板页面显示 

