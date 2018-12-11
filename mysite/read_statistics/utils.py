import datetime  # py自带库
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum 
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
def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    # today - datetime.timedelta(days=1)   # 现在时间 减去固定时间差量（一天）  得到昨天
    read_nums = []
    dates = []
    for i in range(7,0,-1):  # 获得今天以前前7天的数据
        date = today - datetime.timedelta(days=i) 
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date) # 得到所有该天被阅读的类型的次数
        result = read_details.aggregate(read_num_sum=Sum('read_num')) # 得到每天所有被访问的类型访问次数和 result['read_num_sum']是求出的和
        read_nums.append(result['read_num_sum'] or 0) # 如果没有数据 那么取和为 0 
        dates.append(date.strftime('%m/%d')) # 把date变成字符串(格式化) 然后在添加到dates中 
    return dates,read_nums