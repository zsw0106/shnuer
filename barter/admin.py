from django.contrib import admin
from .models import BarterType,Barter,Application

# Register your models here.
@admin.register(BarterType)
class BarterTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name', 'image')

@admin.register(Barter)
class BarterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'barter_type', 'seller', 'image','want_barter','get_read_num', 'created_time', 'last_updated_time','where','status')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id','seller', 'sell_barter', 'buyer', 'buy_barter', 'status', 'isDelete')