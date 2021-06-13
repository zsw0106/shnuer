import datetime
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum,Q
from django.core.cache import cache
from django.urls import reverse
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from notifications.models import Notification
from django.core.paginator import Paginator
from bbs.models import BBS
from barter.models import Barter


def get_7_days_hot_barters():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    barters = Barter.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'name') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return barters[:7]

def get_7_days_hot_bbss():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    bbss = BBS.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return bbss[:7]

def home(request):
    bbs_content_type = ContentType.objects.get_for_model(BBS)
    dates, read_nums = get_seven_days_read_data(bbs_content_type)

    barter_content_type = ContentType.objects.get_for_model(Barter)
    hpdates, hpread_nums = get_seven_days_read_data(barter_content_type)

    # 获取7天热门博客的缓存数据
    hot_bbss_for_7_days = cache.get('hot_bbss_for_7_days')
    if hot_bbss_for_7_days is None:
        hot_bbss_for_7_days = get_7_days_hot_bbss()
        cache.set('hot_bbss_for_7_days', hot_bbss_for_7_days, 3600)

    hot_barters_for_7_days = cache.get('hot_barters_for_7_days')
    if hot_barters_for_7_days is None:
        hot_barters_for_7_days = get_7_days_hot_barters()
        cache.set('hot_barters_for_7_days', hot_barters_for_7_days, 3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(bbs_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(bbs_content_type)
    context['hot_bbss_for_7_days'] = hot_bbss_for_7_days

    context['hpdates'] = hpdates
    context['hpread_nums'] = hpread_nums
    context['hptoday_hot_data'] = get_today_hot_data(barter_content_type)
    context['hpyesterday_hot_data'] = get_yesterday_hot_data(barter_content_type)
    context['hot_barters_for_7_days'] = hot_barters_for_7_days
    return render(request, 'home.html', context)

def search(request):
    search_words = request.GET.get('wd', '').strip()
    # 分词：按空格 & | ~
    condition = None
    for word in search_words.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)

    conditionhp = None
    for word in search_words.split(' '):
        if conditionhp is None:
            conditionhp = Q(name__icontains=word)
        else:
            conditionhp = conditionhp | Q(name__icontains=word)
    
    search_bbss = []
    if condition is not None:
        # 筛选：搜索
        search_bbss = BBS.objects.filter(condition, is_delete=0)

    search_barters = []
    if conditionhp is not None:
        # 筛选：搜索
        search_barters = Barter.objects.filter(conditionhp, status=1, isDelete=False)

    # 分页
    paginator = Paginator(search_bbss, 10)
    page_num = request.GET.get('page', 1) # 获取url的页面参数（GET请求）
    page_of_bbss = paginator.get_page(page_num)

    paginatorhp = Paginator(search_barters, 10)
    page_numhp = request.GET.get('pagehp', 1) # 获取url的页面参数（GET请求）
    page_of_barters = paginatorhp.get_page(page_numhp)

    context = {}
    context['search_words'] = search_words
    context['search_bbss_count'] = search_bbss.count()
    context['page_of_bbss'] = page_of_bbss

    context['search_barters_count'] = search_barters.count()
    print(search_barters)
    context['page_of_barters'] = page_of_barters
    return render(request, 'search.html', context)