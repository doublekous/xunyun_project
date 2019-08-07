# coding=utf-8
import sys
import os
import requests
import random
import re
import IPy
import gevent
import aiohttp
import asyncio
from aiohttp import ClientSession

from ip.models import Ip

basepath = os.path.dirname(__file__)


class choice:
    def Sing_RequestQQGJ(IP):
        username = 'lum-customer-hl_8cea7d90-zone-zone1'
        password = 'vxlqxioh3tsb'
        port = 22225
        session_id = random.random()
        proxy = {
            'http': ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' % (username, session_id, password, port)),
            'https': ('https://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' % (username, session_id, password, port))
            }
        headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept - Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': 'https://guanjia.qq.com/online_server/result.html?url=%s' % IP
        }

        url = 'https://cgi.urlsec.qq.com/index.php?m=check&a=check=&url=http://%s' % IP
        response = (requests.post(url=url, proxies=proxy, headers=headers, timeout=30).text.encode('utf-8').decode('unicode_escape'))
        print(response)
        ip = re.findall(r'\d+.\d+.\d+.\d+', response)
        wordingtitle = re.findall(r'"WordingTitle":(.*),"Wording"', response)
        if len(wordingtitle[0]) == 2:
            wordingtitle[0] = 'IP safety'
        else:
            wordingtitle[0] = "There is something wrong with the IP"
        Ip.objects.create(ip=ip[0], ip_status=wordingtitle[0], comment=1)
        result = ip + wordingtitle
        return result


    async def Muti_RequestQQGJ(IP,num_retries=3):

        username = 'lum-customer-hl_8cea7d90-zone-zone1'
        password = 'vxlqxioh3tsb'
        port = 22225
        session_id = random.random()
        proxy = {
            'http': ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' % (username, session_id, password, port)),
            'https': ('https://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' % (username, session_id, password, port))
            }  # aiohttp不支持此种代理格式
        headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept - Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': 'https://guanjia.qq.com/online_server/result.html?url=%s' % IP
        }
        url = 'https://cgi.urlsec.qq.com/index.php?m=check&a=check=&url=http://%s' % IP
        global res
        async with ClientSession() as session:
            try:
                async with await session.get(url,
                                       proxy="http://lum-customer-hl_8cea7d90-zone-zone1-session-random.random():vxlqxioh3tsb@zproxy.lum-superproxy.io:22225",
                                       headers=headers,timeout=30) as response:
                    response = await response.text()
                    res =response.encode('utf-8').decode("unicode_escape")
                    #print(res)
                    #return res
            except Exception as e:
                if num_retries > 0:
                    # 如果异常就重试
                    await choice.Muti_RequestQQGJ(IP, num_retries - 1)
                else:
                    #重试完毕还有异常，返回异常IP信息
                    #response= {'url':'http:\/\/%s'%IP,'WordingTitle':'未完成检查','Wording':''}
                    #res= str(response)
                    res = '%s未完成检查'%IP
            return res


    async def OpenFile(file):
        uploadfile =  os.path.join(basepath,'upload_file')
        resultfile = os.path.join(basepath, 'result_file')
        file_result = open('%s\\%s' %(resultfile ,file),'a+')
        tasks = []
        semaphore = asyncio.Semaphore(500)
        with open('%s\\%s' %(uploadfile ,file), 'r')as file_request:  # 打开文件
            for line in file_request.readlines():
                line = line.strip('\n')
                if not len(line) or line.startswith('#'):  # 判断是否是空行或注释行
                    continue  # 是的话，跳过不处理
                elif (re.findall(r"\/", line)):  # 匹配CIDR格式
                    ips = IPy.IP(line, make_net=1)
                    for ip in ips:
                        coroutine = choice.Muti_RequestQQGJ(ip)
                        task = asyncio.ensure_future(coroutine)
                        tasks.append(task)
                        responses = await asyncio.gather(*tasks)
                        #print(responses)

                else:  #匹配正常IP
                    coroutine = choice.Muti_RequestQQGJ(line)
                    task = asyncio.ensure_future(coroutine)
                    tasks.append(task)
                    responses = await asyncio.gather(*tasks,return_exceptions=True)
                    #print(responses)

            for data in responses:
                if (re.findall('未完成检查',data)):
                    result=data
                else:
                    ip = re.findall(r'\\\/\\\/(.*),"whitetype"', data)
                    wordingtitle = re.findall(r'"WordingTitle":(.*),"Wording"', data)
                    # wording = re.findall(r'"Wording":(.*),"detect_time"', data)
                    result = ip + wordingtitle
                file_result.writelines(str(result) + '\n')
        file_result.close()
