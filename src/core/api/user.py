import logging
import json
import urllib
from libs import baseview
from libs import util
from core.task import grained_permissions
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.db.models import Count
from rest_framework_jwt.settings import api_settings
from core.models import (
    Account,
    Usermessage,
    Todolist,
    grained
)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
PERMISSION = {
    'ddl': '0',
    'ddlcon': [],
    'dml': '0',
    'dmlcon': [],
    'dic': '0',
    'diccon': [],
    'dicedit': '0',
    'query': '0',
    'querycon': [],
    'user': '0',
    'base': '0',
    'dicexport': '0',
    'person': []
}



class generaluser(baseview.BaseView):
    '''

    :argument 普通用户修改密码

    '''

    def post(self, request, args=None):
        if args == 'changepwd':
            try:
                username = request.data['username']
                old_password = request.data['old']
                new_password = request.data['new']
            except KeyError as e:
                return HttpResponse(status=400)
            else:
                try:
                    user = authenticate(username=username, password=old_password)
                    if user is not None and user.is_active:
                        user.set_password(new_password)
                        user.save()
                        return Response('%s--密码修改成功!' % username)
                    else:
                        return Response('%s--原密码不正确请重新输入' % username)
                except Exception as e:
                    return HttpResponse(status=500)

    def put(self, request, args: str = None):
        try:
            mail = request.data['mail']
        except KeyError as e:
            return HttpResponse(status=400)
        else:
            try:
                Account.objects.filter(username=request.user).update(email=mail)
                return Response('邮箱地址已更新!')
            except Exception as e:
                return HttpResponse(status=500)


class authgroup(baseview.BaseView):
    '''

    认证组权限

    '''

    @grained_permissions
    def post(self, request, args=None):
        try:
            _type = request.data['permissions_type'] + 'edit'
            permission = grained.objects.filter(username=request.user).first()
            return Response(permission.permissions[_type])
        except Exception as e:
            return HttpResponse(status=500)





class login_auth(baseview.AnyLogin):

    def post(self, request, args: str = None):

        '''
        普通登陆类型认证
        :return: jwt token888
        '''
        try:
            permissions = {'querycon': [], 'user': '1', 'base': '1', 'dicexport': '0'}
            username = request.data['username']
            password = request.data['password']
        except KeyError as e:
            return HttpResponse(status=400)
        else:
            permissions = authenticate(username=username, password=password)
            if permissions is not None and permissions.is_active:
                token = jwt_encode_handler(jwt_payload_handler(permissions))
                return Response(
                    {'token': token, 'name': username, 'user': username,
                     'group': 'admin'},
                    status=201)
            else:
                return HttpResponse(status=400)
