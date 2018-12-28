from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType 
from django.utils import timezone

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0) # 阅读次数

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # models.CASCADE 删除阅读次数会删除博客   DO_NOTHING  删除阅读次数对应博客本身无影响
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpandMethod():   # 封装了一个类 以后要用到下面的方法继承这个类就行
    def get_read_num(self):   # 新增得到阅读数的方法
        try:                 # 会先完成try中的代码 如果完成中发生获取不到的错误 执行后一条
            ct = ContentType.objects.get_for_model(self) # 获取关联到Blog的 ContentType 实例
            readnum = ReadNum.objects.get(content_type = ct ,object_id = self.pk)  # 获得所有关联到Blog ， id值= self.pk 这个blog的 ReadNum 
            return readnum.read_num    # 查看这一条记录的阅读次数
        except exceptions.ObjectDoesNotExist:  # except Exception as e  不管什么错误都会获取    
            return 0                        # exceptions.ObjectDoesNotExist  记录不存在的错误返回 0

class ReadDetail(models.Model):  
    date = models.DateField(default=timezone.now) # 时间
    read_num = models.IntegerField(default=0) 

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')