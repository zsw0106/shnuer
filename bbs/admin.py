from django.contrib import admin
from .models import BBSType, BBS

@admin.register(BBSType)
class BBSTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(BBS)
class BBSAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'bbs_type', 'author', 'get_read_num', 'created_time', 'last_updated_time')
