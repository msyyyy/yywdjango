#  阅读计数统计和显示

## 显示每一天的访问量

> 1. 在`read_statistics/models.py`加入新的模型
```python
class ReadDetail(models.Model):  
    date = models.DateField(default=timezone.now) # 时间
    read_num = models.IntegerField(default=0) 

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
```

> 2. 修改`utils.py`文件 增加修改访问量的方法

#### 方法一 

```python
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReadNum,ReadDetail

def read_statistics_once_read(request, obj): # 这里传 obj是为了告诉ContentType 传进来的与Blog还是其他什么对应
    ct = ContentType.objects.get_for_model(obj)
    key ="%s_%s_read" % (ct.model, obj.pk)   # 对应应该有的cookie值

    if not request.COOKIES.get(key): # 还没阅读过
        if ReadNum.objects.filter(content_type = ct ,object_id = obj.pk).count():  # 检测这个阅读数记录是否存在 
            # 存在
            readnum = ReadNum.objects.get(content_type = ct ,object_id = obj.pk) # 挑选出这条记录
        else:
            # 不存在对应记录
            readnum = ReadNum(content_type = ct ,object_id = obj.pk)  # 实例化
        # 计数加1   
        readnum.read_num += 1 
        readnum.save()  # 保存

        # 分日期的访问量
        date = timezone.now().date()  # .now包含时分秒  在.date() 就只包含日期
        if ReadDetail.objects.filter(content_type=ct,object_id = obj.pk,date=date).count():
            readDetail = ReadDetail.objects.get(content_type=ct,object_id = obj.pk,date=date)
        else:
            readDetail = ReadDetail(content_type=ct,object_id = obj.pk,date=date)
        readDetail.read_num += 1
        readDetail.save()

    return key  # 最后返回的是一个cookie标记
```

#### 方法二  get_or_create  获取元组 或者 创建
```python
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReadNum,ReadDetail

def read_statistics_once_read(request, obj): # 这里传 obj是为了告诉ContentType 传进来的与Blog还是其他什么对应
    ct = ContentType.objects.get_for_model(obj)
    key ="%s_%s_read" % (ct.model, obj.pk)   # 对应应该有的cookie值

    if not request.COOKIES.get(key): # 还没阅读过
        readnum , created = ReadNum.objects.get_or_create(content_type = ct ,object_id = obj.pk)  # 返回对象 和 是否是创建 创建 created = True
        readnum.read_num += 1  # 计数加1  
        readnum.save()  # 保存

        # 当天阅读数+1
        date = timezone.now().date()  # .now包含时分秒  在.date() 就只包含日期
        readDetail , created = ReadDetail.objects.get_or_create(content_type=ct,object_id = obj.pk,date=date)
        readDetail.read_num += 1
        readDetail.save()

    return key  # 最后返回的是一个cookie标记
```

成功显示每天阅读数

> 所有博客阅读数之和  该天与前七天的阅读数作对比

`shell`
```
rds = ReadDetail.objects().all() # 阅读次数模型的实例

rds.aggregate(read_num_sum=Sum('read_num')) # 对所有实例的read_num属性求和 最后返回字典 read_num_sum 对应一个数字
```
`utils.py`
```python
from django.db.models import Sum 

def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    # today - datetime.timedelta(days=1)   # 现在时间 减去固定时间差量（一天）  得到昨天
    read_nums = []
    for i in range(7,0,-1):  # 获得今天以前前7天的数据
        date = today - datetime.timedelta(days=i) 
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date) # 得到所有该天被阅读的类型的次数
        result = read_details.aggregate(read_num_sum=Sum('read_num')) # 得到每天所有被访问的类型访问次数和 result['read_num_sum']是求出的和
        read_nums.append(result['read_num_sum'] or 0) # 如果没有数据 那么取和为 0 
    return read_nums
```

`mysite/views.py`

```python
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_date
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog) # 获得关联到Blog类型的 ContentType实例
    read_nums = get_seven_days_read_date(blog_content_type)    # 获得前七天博客阅读的list
    context={}
    context['read_nums'] = read_nums
    return render_to_response('home.html',context)
```

现在能得到前7天的数据了 但是只有数据 太丑 



