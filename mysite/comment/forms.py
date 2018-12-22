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