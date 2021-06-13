from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.http import HttpResponseRedirect 
from datetime import *
from django.core.mail import send_mail
from django.core.paginator import Paginator

from .models import Barter, BarterType, Application
from read_statistics.utils import read_statistics_once_read
from .forms import BarterForm

# Create your views here.
def barter_list(request):
    # 取出所有换品
    barters = Barter.objects.filter(status='1',isDelete=False)
    paginator = Paginator(barters, 9)
    page_num = request.GET.get('page', 1) # 获取url的页面参数（GET请求）
    page_of_barters = paginator.get_page(page_num)
    # 需要传递给模板（templates）的对象
    context = {}
    context['page_of_barters'] = page_of_barters
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
    return HttpResponseRedirect('/barter/my_application')

# 个人换品
def personal_barters(request):
    barters = Barter.objects.filter(seller=request.user, isDelete=False)
    paginator = Paginator(barters, 9)
    page_num = request.GET.get('page', 1) # 获取url的页面参数（GET请求）
    page_of_barters = paginator.get_page(page_num)
    # 需要传递给模板（templates）的对象
    context = {}
    context['page_of_barters'] = page_of_barters
    context['user'] = request.user
    return render(request, 'barter/personal_barters.html', context)

# 个人换品的申请和被申请
def my_application(request):
    myapplications = Application.objects.filter(seller=request.user)
    my_applys = Application.objects.filter(buyer=request.user)
    context = {'myapplications':myapplications}
    context['my_applys'] = my_applys
    return render(request,'barter/application.html', context)

# 同意换品申请
def recive_apply(request):
    order_id = request.POST.get('data');
    Application.objects.filter(order_id=order_id).update(status=2)
    sell_barter = Application.objects.filter(order_id=order_id).first().sell_barter
    sell_barter.status = 0
    sell_barter.save()
    buy_barter = Application.objects.filter(order_id=order_id).first().buy_barter
    buy_barter.status = 0
    buy_barter.save()
    seller_email = Application.objects.filter(order_id=order_id).first().seller.email
    buyer_email = Application.objects.filter(order_id=order_id).first().buyer.email
    send_mail('SHNU：交换成功', '这是卖家的邮箱' + str(seller_email), '3425226666@qq.com', [str(buyer_email)], fail_silently=False)
    data = "成功"
    return JsonResponse({'data':data})

# 拒绝换品申请
def reject_apply(request):
    order_id = request.POST.get('data');
    Application.objects.filter(order_id=order_id).update(status=1)
    data = "拒绝成功"
    return JsonResponse({'data':data})


def add_barter(request):
    if request.method == 'POST':
        barter_form = BarterForm(request.POST, request.FILES)
        if barter_form.is_valid():
            barter_form.instance.seller = request.user #获取登录用户实例，发布换品
            barter_form.save()
            return redirect(request.GET.get('from', reverse('barter_list')))
    else:
        barter_form = BarterForm()
    return render(request, 'barter/add_barter.html', {'barter_form':barter_form})

# 删换品
def barter_delete(request, id):
    # 根据 id 获取需要删除的文章
    barter = Barter.objects.get(id=id)
    # 调用.delete()方法删除文章
    barter.isDelete = True
    barter.save()
    # 完成删除后返回文章列表
    return redirect("barter_list")

# 更新换品
def barter_update(request, id):
    barter = Barter.objects.get(id=id)
    if request.method != 'POST':
        # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
        form = BarterForm(instance=barter) 
    else:
  # 如果是post,instance=article当前数据填充表单，并用data=request.POST获取到表单里的内容
        form = BarterForm(instance=barter, data=request.POST, files=request.FILES)
        print(request.FILES)
        form.save() # 保存
        if form.is_valid(): # 验证
            return redirect('barter_detail',barter.pk) # 成功跳转
    return render(request, 'barter/barter_update.html', {'form':form,'barter':barter})
