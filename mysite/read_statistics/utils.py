from django.contrib.contenttypes.models import ContentType
from .models import ReadNum

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
    return key  # 最后返回的是一个cookie标记