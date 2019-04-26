from django.db import models

# Create your models here.
# super_table表
class Super_Table(models.Model):
    id = models.AutoField(primary_key=True)      # 序号，自增
    name = models.CharField(max_length=64)      # 姓名
    tel = models.CharField(max_length=16)       # 联系方式
    address = models.CharField(max_length=200)      # 地址

    # 联合唯一，要求姓名与联系方式的组合必须唯一
    class Meta:
        unique_together = ('name', 'tel')
