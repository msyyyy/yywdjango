from django import  forms 
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(
                                            attrs={'class':'form-control','placeholder':'请输入用户名'}))# 默认显示为username我们让他显示为用户名 , require 默认为True 这个是如果不没填写用户名他会提醒你
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(
                                            attrs={'class':'form-control','placeholder':'请输入用户名'})) # 密文输入显示

    # 清理有问题数据,返回的一定是有效数据
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password'] # 获取填写的账号密码

        user = auth.authenticate(username=username,password=password) # 验证数据库中是否有对应账号密码
        if user is  None:  # 如果不存在,返回一个错误
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user # 存在 那么返回user
        return self.cleaned_data

# 注册
class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                                max_length=30,
                                min_length=3,
                               widget=forms.TextInput(
                                            attrs={'class':'form-control','placeholder':'请3-30位输入用户名'}))
    email = forms.CharField(label='邮箱',
                               widget=forms.EmailInput(
                                            attrs={'class':'form-control','placeholder':'请输入邮箱'}))
    password  = forms.CharField(label='密码',
                                min_length=6,
                               widget=forms.PasswordInput(
                                            attrs={'class':'form-control','placeholder':'请输入密码'}))
    password_again  = forms.CharField(label='再输入一次密码',
                                        min_length=6,
                                        widget=forms.PasswordInput(
                                            attrs={'class':'form-control','placeholder':'再一次输入密码'}))

    # 判断用户名是否被注册
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    # 判断邮箱已被注册
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    # 验证两遍密码是否一致
    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password !=password_again:
            raise forms.ValidationError('两次密码不一致')
        return password


    