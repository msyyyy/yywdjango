from django.urls import path
from . import views
urlpatterns = [
    # localhost:8000/article/
    path('',views.article_list,name="article_list"),
    # localhost:8000/article/<int:article_id>
    path('<int:article_id>',views.article_detail,name="article_detail"),
]
