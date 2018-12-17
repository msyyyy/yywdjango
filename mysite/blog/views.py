from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator #分页器
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from .models import Blog,BlogType
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm

def get_blog_list_common_date(request,blogs_all_list):
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) # 每几篇文章进行分页
    page_num = request.GET.get('page',1) # 获取页码参数（GET请求）
    page_of_blogs = paginator.get_page(page_num) # 如果得到的是非法页码自动返回 1
    currentr_page_num = page_of_blogs.number # 获取当前页码
    page_range=[x for x in range(int(page_num)-2, int(page_num)+3  )  if 0<x<=paginator.num_pages] # 获取当前页的前后两页

    
    if page_range[0] -1 >=2:   # 加上省略号
        page_range.insert(0,'...')
    if paginator.num_pages -page_range[-1] >=2:
        page_range.append('...')

    if page_range[0] !=1:   # 如果page_range没有1号页码 增加一个1号页码按钮
        page_range.insert(0,1)
    if page_range[-1] !=paginator.num_pages:     # 如果page_range没有最后页码 
        page_range.append (paginator.num_pages)

    # 获得日期归档对应的博客数量
    blog_dates =  Blog.objects.dates('created_time','month',order="DESC")
    blog_dates_dict = {}   # 字典,相当于c++map
    for blog_date in blog_dates:
        #找出所有存在的年月 的博客数量
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count  # 将年月和博客数量对应

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs  # 传入分页信息
    context['page_range'] = page_range
    # 获取博客分类的对应博客数目
    # context['blog_types'] = BlogType.objects.annotate( blog_count = Count('blog')) # SQL语句等访问时再执行  Blog通过外键相关连了BlogType
    context['blog_types'] = BlogType.objects.all()

    context['blog_dates'] = blog_dates_dict 
    return context

def blog_list(request):
    blogs_all_list=Blog.objects.all()
    context = {}
    context = get_blog_list_common_date(request,blogs_all_list)
    return render( request,'blog/blog_list.html',context)


def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list=Blog.objects.filter(blog_type=blog_type)
    context = {}
    context = get_blog_list_common_date(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render( request,'blog/blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    blogs_all_list=Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = {}
    context = get_blog_list_common_date(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year,month)
    return render( request,'blog/blogs_with_date.html',context)

def blog_detail(request,blog_pk):
    
    blog = get_object_or_404(Blog,pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog) 
    blog_content_type = ContentType.objects.get_for_model(blog) # 获取与Blog相关联的cotenttype
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk) # 获取对应该博客的评论

    context = {}    
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last() # 获取上一篇博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 获取下一篇博客 
    context['blog'] = blog
    context['comments'] = comments
    context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id': blog_pk})#  提交评论 传入字典给评论的content_type和object_id赋初值
    response = render( request,'blog/blog_detail.html',context) # 响应
    response.set_cookie(read_cookie_key,'true' ) # 键值  权值   max_age有效期持续时间   expires 有效期到多久为止,
    #有了expires 则 max_age 无效 如果两个都不设置  那么打开浏览器时一直有效 关闭浏览器失效 
    return response
