from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from .models import BBS, BBSType
from read_statistics.utils import read_statistics_once_read
from .forms import BBSForm


def get_bbs_list_common_data(request, bbss_all_list):
    paginator = Paginator(bbss_all_list, settings.EACH_PAGE_BBSS_NUMBER)
    page_num = request.GET.get('page', 1) # 获取url的页面参数（GET请求）
    page_of_bbss = paginator.get_page(page_num)
    currentr_page_num = page_of_bbss.number # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取日期归档对应的博客数量
    bbs_dates = BBS.objects.dates('created_time', 'month', order="DESC")
    bbs_dates_dict = {}
    for bbs_date in bbs_dates:
        bbs_count = BBS.objects.filter(created_time__year=bbs_date.year, 
                                         created_time__month=bbs_date.month).count()
        bbs_dates_dict[bbs_date] = bbs_count

    context = {}
    context['bbss'] = page_of_bbss.object_list
    context['page_of_bbss'] = page_of_bbss
    context['page_range'] = page_range
    context['bbs_types'] = BBSType.objects.annotate(bbs_count=Count('bbs'))
    context['bbs_dates'] = bbs_dates_dict
    return context

def bbs_list(request):
    bbss_all_list = BBS.objects.all()
    context = get_bbs_list_common_data(request, bbss_all_list)
    return render(request, 'bbs/bbs_list.html', context)

def bbss_with_type(request, bbs_type_pk):
    bbs_type = get_object_or_404(BBSType, pk=bbs_type_pk)
    bbss_all_list = BBS.objects.filter(bbs_type=bbs_type)
    context = get_bbs_list_common_data(request, bbss_all_list)
    context['bbs_type'] = bbs_type
    return render(request, 'bbs/bbss_with_type.html', context)

def bbss_with_date(request, year, month):
    bbss_all_list = BBS.objects.filter(created_time__year=year, created_time__month=month)
    context = get_bbs_list_common_data(request, bbss_all_list)
    context['bbss_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'bbs/bbss_with_date.html', context)

def bbs_detail(request, bbs_pk):
    bbs = get_object_or_404(BBS, pk=bbs_pk)
    read_cookie_key = read_statistics_once_read(request, bbs)

    context = {}
    context['previous_bbs'] = BBS.objects.filter(created_time__gt=bbs.created_time).last()
    context['next_bbs'] = BBS.objects.filter(created_time__lt=bbs.created_time).first()
    context['bbs'] = bbs
    response = render(request, 'bbs/bbs_detail.html', context) # 响应
    response.set_cookie(read_cookie_key, 'true') # 阅读cookie标记
    return response

# 添加帖子
def add_bbs(request):
    if request.method == 'POST':
        bbs_form = BBSForm(request.POST)
        if bbs_form.is_valid():
            bbs_form.instance.author = request.user #获取登录用户实例，创建帖子
            bbs_form.save()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        bbs_form = BBSForm()
    return render(request, 'bbs/add_bbs.html', {'bbs_form':bbs_form})