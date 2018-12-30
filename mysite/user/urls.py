from django.urls import path
from . import  views

urlpatterns = [
    path('login_for_medal/',views.login_for_medal, name='login_for_medal'), # 从点赞登录
    path('login/',views.login, name='login'), # 登录界面
    path('register/',views.register, name='register'), # 注册
    path('logout/',views.logout, name='logout'), # 登出
    path('user_info/',views.user_info, name='user_info'), # 用户个人信息
]
