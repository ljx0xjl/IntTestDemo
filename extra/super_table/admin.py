from django.contrib import admin
from super_table.models import Super_Table      # 引入Super_Table

# Register your models here.
class STAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'tel', 'address']     # 管理页面显示项目种类
    search_fields = ['name']        # 启用搜索栏

admin.site.register(Super_Table, STAdmin)       # 注册


