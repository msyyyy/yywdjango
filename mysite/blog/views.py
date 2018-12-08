from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator #分页器
from .models import Blog,BlogType
from django.conf import settings

def blog_list(request):

    blogs_all_list=Blog.objects.all()
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

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs  # 传入分页信息
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog,pk=blog_pk)
    return render_to_response('blog/blog_detail.html',context)

def blogs_with_type(request,blog_type_pk):

    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list=Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) 
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

    context = {}
    context['blog_type'] = blog_type
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs  # 传入分页信息
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()

    return render_to_response('blog/blogs_with_type.html',context)