# 回复功能 和 树结构

评论可被回复  回复可被回复

> 创建 评论对象级数和评论对象的外键

为了解决两个相同外键冲突问题 增加 related_name
```python
 user = models.ForeignKey(User, related_name="comments",on_delete=models.DO_NOTHING) # 评论者
# 他的评论对象级数 指向自己  允许为空(为空就是指向博客)
 parent = models.ForeignKey('self',null=True,on_delete=models.DO_NOTHING)
# 回复谁,评论对象
reply_to = models.ForeignKey(User, related_name="replies",null=True,on_delete=models.DO_NOTHING)

```