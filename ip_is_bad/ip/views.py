import csv
import json
from ipaddress import IPv4Network

import pandas as pd
from IPy import IP
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from gevent.pool import Pool


from ip.models import Ip
from utils.choice import choice
from utils.common import Pagenate
from utils.many_ip import get_ip


# /ip/ip_query
class Ip_queryView(View):
    """检测ip状态"""
    def get(self, request):
        return render(request, 'ip/ip_query.html')

    @transaction.atomic
    def post(self, request):
        """检测ip状态"""
        save_ip = transaction.savepoint()
        try:
            Ip.objects.select_for_update().filter(comment=1).update(comment=0)
            update_ip_query_list = []
            ip_query = request.POST.get('ip_query')
            if len(ip_query) == 0:
                CODE = 201
                error = '请在空白处输入ip'
            try:
                ip_query_list = [i for i in ip_query.split('\n') if i]
                print(ip_query_list)
                pool = Pool(100)
                single_ip = pool.map(choice.Sing_RequestQQGJ, ip_query_list)
                update_ip_query_list.append(single_ip)
                CODE = 200
                error = ''
            except Exception as e:
                CODE = 202
                error = '请输入正确的ip格式'
            # print(update_ip_query_list)
        except Ip.DoesNotExist:
            transaction.savepoint_rollback(save_ip)
        transaction.savepoint_commit(save_ip)
        return HttpResponse(json.dumps({'code': CODE, 'update_ip_query_list': update_ip_query_list, 'error': error}))
        # return render(request, 'ip/ip_query.html', locals())


# /ip/search_ip
class Search_ipView(View):
    """过滤展示"""
    def post(self, request):
        """过滤ip"""
        search_dict = {}
        searchdatas = []
        ip_query = request.POST.get('ip_query')
        page = int(request.POST.get('page', '1'))
        page_n = 10 * (page - 1)
        page_m = 10 * page
        s = Q()
        ip_query_list = [i for i in ip_query.split('\n') if i]
        if len(ip_query_list) != 0:
            dict_ip = {'ip': ip_query_list}
            for q in dict_ip:
                for i in dict_ip[q]:
                    s.add(Q(**{q: i}), Q.OR)
        search_data = Ip.objects.filter(s).all()
        if len(search_data) == 0:
            CODE = 203
            error = 'ip检测尚未完成'
        # Ip.objects.filter(s).update(comment=1)
        search_data_page = len(search_data)
        if len(ip_query_list) == 0:
            search_data = Ip.objects.all()
        for s in search_data[page_n: page_m]:
            CODE = 200
            error = ''
            searchdatas.append({
                'id': s.id,
                'ip': s.ip,
                'ip_status': s.ip_status
            })
        print(searchdatas)
        page_items = Pagenate(page, range(0, search_data_page), 10).json_result()
        return HttpResponse(json.dumps({'code': CODE, 'searchdatas': searchdatas, 'page_items': page_items, 'error': error}))


# /ip/export_ip
def export_ip(request):
    '''导出ip'''
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="error_ip.csv"'
    writer = csv.writer(response, dialect='excel')
    writer.writerow(map(lambda x: x.encode('utf-8').decode('utf-8'), [
        'IP', 'ip_status'
    ]))
    ips = Ip.objects.filter(comment=1).all()
    for ip in ips:
        new_ip = [
            ip.ip,
            ip.ip_status
        ]
        print(new_ip)
        writer.writerow(map(lambda x: x, new_ip))
    return response


# /ip/upload_ip
class Upload_ipView(View):
    """上传ip文件检测"""
    @transaction.atomic
    def post(self, request):
        """上传ip文件检测"""
        ip_query_list = []
        update_ip_query_list = []
        save_ip = transaction.savepoint()
        try:
            Ip.objects.filter(comment=1).update(comment=0)
            file_obj = request.FILES.get('file_upload_trumpl')
            # 读取文件
            df = pd.read_csv(file_obj)
            list_data = df.values.tolist()
            for item in list_data:
                ip_query_list.append(item[0])
            pool = Pool(100)
            single_ip = pool.map(choice.Sing_RequestQQGJ, ip_query_list)
        except Ip.DoesNotExist:
            transaction.savepoint_rollback(save_ip)
        transaction.savepoint_commit(save_ip)
        # return HttpResponse(json.dumps({'code': 200, 'single_ip': single_ip}))
        return HttpResponse('<a href="/ip/ip_query/">上传ip成功点我返回下载异常ip</a>')


# /ip/continuous_ip
class Continuous_ipView(View):
    """连续ip查询"""
    def post(self, request):
        """查询连续ip"""
        continuous_ip = request.POST.get('continuous_ip')
        try:
            ip_list = get_ip(continuous_ip)
            pool = Pool(100)
            single_ip = pool.map(choice.Sing_RequestQQGJ, ip_list)
            CODE = 200
            error = ''
        except Exception as e:
            single_ip = []
            CODE = 205
            error = '请检查输入ip的格式'
        return HttpResponse(json.dumps({'code': CODE, 'single_ip': single_ip, 'error': error}))