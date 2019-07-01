__author__ = 'nanfeng'
import json
import logging
from django.http import HttpResponse
import random
from jinja2 import PackageLoader,Environment,FileSystemLoader
import re

from rest_framework.response import Response
from libs import baseview
from .nginxtemplate import nginxrender
from libs import util
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from rest_framework import viewsets,status, generics

from core.models import nginxinfo
from rest_framework.pagination import PageNumberPagination
from .serializers import NginxInfoSerializer
from .salt_api import sync
nginx_conf_path = "/alidata/server/nginx/conf"
class CommonPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class TargetHostView(baseview.BaseView):
    def get(self, request, args: str = None):
        templist = []
        for host in sync('*', 'cmd.run', 'hostname').keys():
            tempdict = {}
            tempdict['label'] = host
            tempdict['value'] = host
            templist.append(tempdict)
        return Response(templist,status=200)
class NginxServiceView(baseview.BaseView):
    def post(self, request, args: str = None):
        if args == 'check':
            try:
                hostlist = request.data['hostlist']
                title = request.data['title']
            except KeyError as e:
                pass
            else:
                templist = []
                for host in hostlist:
                    if int(sync(host, 'cmd.run', 'ps -ef | grep nginx|grep -v grep |wc -l')[host]) >= 1:
                        value = request.data['nginxinfo']
                        value['othervalue'] = value['othervalue'].replace('\n', '\n' + '    ')
                        try:
                            for line in value['regurllist']:
                                line['otherparameter'] = line['otherparameter'].replace('\n', '\n' + '        ')
                        except Exception as e:
                            pass
                        result = nginxrender(value)
                        sync('test-xiaolongxia', 'file.remove',
                             '{}/vhosts/{}.conf'.format(nginx_conf_path, title))
                        sync('test-xiaolongxia', 'file.touch',
                             '{}/vhosts/{}.conf'.format(nginx_conf_path,title))
                        sync('test-xiaolongxia', 'file.append',
                             ['{}/vhosts/{}.conf'.format(nginx_conf_path, title), result])
                        nginxtestinfo = sync(host, 'cmd.run', '/alidata/server/nginx/sbin/nginx -t')[
                            host].replace('\n', '<br>')
                        return Response(
                            '<b>nginx进程</b>： <font color="OOOOFF">存在</font><br> <b>文件需要覆盖</b>:<font color="red"> 是</font><br> <b>文件测试信息</b>:<br> %s' % nginxtestinfo)
        if args == 'preview':
            value = request.data
            value['othervalue'] = value['othervalue'].replace('\n', '\n' + '    ')
            try:
                for line in value['regurllist']:
                    line['otherparameter'] = line['otherparameter'].replace('\n', '\n' + '        ')
            except Exception as e:
                pass
            result = nginxrender(value)
            return Response(result, status=201)
        if args == 'reload':
            try:
                host = request.data['host']
            except KeyError as e:
                return Response({'log': '缺少指定的主机'}, status=400)
            else:
                result = sync(host, 'cmd.run', '/alidata/server/nginx/sbin/nginx -s reload')[host]
                if result == '':
                    return Response(status=201)
                else:
                    return Response({'log':result },status=400)
class nginx_checkView(baseview.BaseView):
    def post(self, request, args: str = None):
        hostlist = request.data['hostlist']
        title = request.data['title']
        for host in hostlist:
            if int(sync(host, 'cmd.run', 'ps -ef | grep nginx|grep -v grep |wc -l')[host]) >=1:
                value = request.data['nginxinfo']
                value['othervalue'] = value['othervalue'].replace('\n', '\n' + '    ')
                try:
                    for line in value['regurllist']:
                        line['otherparameter'] = line['otherparameter'].replace('\n', '\n' + '        ')
                except Exception as e:
                    pass
                result = nginxrender(value)
                sync(host, 'file.remove', '{}/vhosts/{}.conf'.format(nginx_conf_path,title))
                sync(host, 'file.touch', '{}/vhosts/{}.conf'.format(nginx_conf_path,title))
                sync(host, 'file.append', ['{}/vhosts/{}.conf'.format(nginx_conf_path, title), result])
                nginxtestinfo = sync(host, 'cmd.run', '/alidata/server/nginx/sbin/nginx -t')[host].replace('\n', '<br>')
                return Response('<b>nginx进程</b>： <font color="OOOOFF">存在</font><br> <b>文件需要覆盖</b>:<font color="red"> 是</font><br> <b>文件测试信息</b>:<br> %s' % nginxtestinfo)
class NginxFileManager(baseview.BaseView):
    def post(self, request, args: str = None):
        regex = re.compile('\s+')
        if args == 'readdir':
            '''
            如果参数是获取特定文件夹的文件
            '''
            try:
                host = request.data['host']
                filename = request.data.get('filename', None)
            except KeyError as e:
                return Response({'log': '缺少指定的主机'}, status=400)
            else:
                regex = re.compile('\s+')
                progress_list = []
                menu_list = []
                content = {}
                progress_info = sync('test-xiaolongxia', 'cmd.run',
                                     'ls -l --full-time {}/vhosts/'.format(nginx_conf_path))
                if progress_info['test-xiaolongxia']:
                    data_list = progress_info['test-xiaolongxia'].split("\n")
                    del (data_list[0])
                    for data_line in data_list:
                        content = {}
                        content['access'] = regex.split(data_line)[0]
                        if content['access'].startswith('d'):
                            content['file_type'] = '文件夹'
                        else:
                            content['file_type'] = '文本'
                        content['secondfilenum'] = regex.split(data_line)[1]
                        content['group'] = regex.split(data_line)[2]
                        content['user'] = regex.split(data_line)[3]
                        content['size'] = regex.split(data_line)[4]
                        content['date'] = regex.split(data_line)[5]
                        content['modifytime'] = regex.split(data_line)[6]
                        content['filename'] = regex.split(data_line)[8]
                        progress_list.append(content)
                    return Response({'results': progress_list})
                else:
                    return Response(status=400)
        if args == 'fileread':
            '''
            如果是要读取特定文件
            '''
            try:
                host = request.data['host']
                filename = request.data['filename']
            except Exception as e:
                return Response({'log': '缺少指定的主机或者具体文件名'}, status=400)
            else:
                if sync(host, 'file.file_exists', '{}/vhosts/{}'.format(nginx_conf_path,filename))[host]:
                    filecontent = sync(host, 'cmd.run', 'cat {}/vhosts/a{}'.format(nginx_conf_path, filename))[host]
                    fileresult = sync('test-xiaolongxia', 'cmd.run',
                                      'ls -l --full-time {}/vhosts/{}'.format(nginx_conf_path,filename))[host]
                    data_list = fileresult.split("\n")
                    now_modifytime = regex.split(data_list[0])[6]
                    return Response({'results': filecontent, 'modifytime': now_modifytime})
                else:
                    return Response({'log': '文件不存在或者通信失败，加载失败'}, status=400)
        if args == 'filesave':
            try:
                host = request.data['host']
                filename = request.data['filename']
                filecontent = request.data['filecontent']
                modifytime = request.data['modifytime']
                print(request.data)
            except KeyError as e:
                return Response({'log': '缺少指定的主机或者具体文件名或者文件内容'}, status=400)
            else:
                result = sync(host, 'file.file_exists', '{}/vhosts/{}'.format(nginx_conf_path,filename))[host]
                if result:
                    fileresult = sync('test-xiaolongxia', 'cmd.run',
                         'ls -l --full-time {}/vhosts/{}'.format(nginx_conf_path,filename))[host]
                    data_list = fileresult.split("\n")
                    now_modifytime = regex.split(data_list[0])[6]
                    if modifytime != now_modifytime:
                        return Response({'log': '检测到服务器上该文件已被其它人修改，请刷新后重新编辑！'}, status=400)
                    else:
                        sync(host, 'file.remove','{}/vhosts/{}'.format(nginx_conf_path,filename))
                        sync(host, 'file.touch','{}/vhosts/{}'.format(nginx_conf_path, filename))
                        sync(host, 'file.append',['{}/vhosts/{}'.format(nginx_conf_path, filename), filecontent])
                        return Response(status=201)
                else:
                    return Response({'log': '文件不存在或者通信失败，加载失败'}, status=400)
        if args == 'delete':
            try:
                host = request.data['host']
                filename = request.data['filename']
                modifytime = request.data['modifytime']
            except KeyError as e:
                return Response({'log': '缺少指定的主机或者具体文件名'}, status=400)
            else:
                result = sync(host, 'file.file_exists', '{}/vhosts/{}'.format(nginx_conf_path,filename))[host]
                if result:
                    fileresult = sync('test-xiaolongxia', 'cmd.run',
                                      'ls -l --full-time {}/vhosts/{}'.format(nginx_conf_path, filename))[host]
                    data_list = fileresult.split("\n")
                    now_modifytime = regex.split(data_list[0])[6]
                    if modifytime != now_modifytime:
                        return Response({'log': '检测到服务器上该文件已被其它人修改，请刷新确认后再删除！'}, status=400)
                    else:
                        delete_result = sync(host, 'file.remove', '{}/vhosts/{}'.format(nginx_conf_path, filename))[host]
                        if delete_result:
                            return Response(status=201)
                        else:
                            return Response({'log': '删除失败！！！'}, status=400)
                else:
                    return Response({'log': '文件不存在或者通信失败，加载失败'}, status=400)



class NginxInfoSaveView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = nginxinfo.objects.all().order_by('-create_time')
    serializer_class = NginxInfoSerializer
    pagination_class = CommonPagination


class nginxView(baseview.BaseView):
    def post(self, request, args: str = None):
        value = request.data
        value['othervalue'] = value['othervalue'].replace('\n', '\n' + '    ')
        try:
            for line in value['regurllist']:
                line['otherparameter'] = line['otherparameter'].replace('\n', '\n' + '        ')
        except Exception as e:
            pass
        result = nginxrender(value)
        return Response(result, status=201)












