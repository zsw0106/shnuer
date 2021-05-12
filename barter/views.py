from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from datetime import *

from .models import Barter, BarterType, Application
from read_statistics.utils import read_statistics_once_read
from .forms import BarterForm

# Create your views here.
def barter_list(request):
    # 取出所有换品
    barters = Barter.objects.filter(status='1')
    # 需要传递给模板（templates）的对象
    context = { 'barters': barters }
    # render函数：载入模板，并返回context对象
    return render(request, 'barter/barter_list.html', context)

def barter_detail(request, barter_pk):
    barter = get_object_or_404(Barter, pk=barter_pk)
    read_cookie_key = read_statistics_once_read(request, barter)
    mybarters = Barter.objects.filter(status='1',seller_id=request.user.id)

    context = {}
    context['previous_barter'] = Barter.objects.filter(created_time__gt=barter.created_time).last()
    context['next_barter'] = Barter.objects.filter(created_time__lt=barter.created_time).first()
    context['barter'] = barter
    context['mybarters'] = mybarters
    response = render(request, 'barter/barter_detail.html', context) # 响应
    response.set_cookie(read_cookie_key, 'true') # 阅读cookie标记
    return response

def barter_with_type(request, barter_type_pk):
    barter_type = get_object_or_404(BarterType, pk=barter_type_pk)
    barters = Barter.objects.filter(barter_type=barter_type)
    context = { 'barters': barters }
    context['barter_type'] = barter_type
    return render(request, 'barter/barter_with_type.html', context)

def apply_barter(request):
    if request.method == "POST":
        buy_barter_id= request.POST.get("select_mybarters",None)
        buy_barter = get_object_or_404(Barter, pk=buy_barter_id)
        buyer = request.user
        barter_pk = request.POST.get("sell_barter",None)
        sell_barter = get_object_or_404(Barter, pk=barter_pk)
        seller = sell_barter.seller
        order_id = datetime.now().strftime('%Y%m%d%H%M%S')+str(buyer.id)
        data = {}
        try:
            Application.objects.create(order_id = order_id, seller = seller, sell_barter = sell_barter, buyer = buyer, buy_barter = buy_barter)
            data['status'] = 'SUCCESS'
        except Exception as e:
            print("error = ",e)
            data['status'] = 'f1'
    return JsonResponse(data)



def add_barter(request):
    if request.method == 'POST':
        barter_form = BarterForm(request.POST, request.FILES)
        if barter_form.is_valid():
            barter_form.instance.seller = request.user #获取登录用户实例，发布换品
            barter_form.save()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        barter_form = BarterForm()
    return render(request, 'barter/add_barter.html', {'barter_form':barter_form})