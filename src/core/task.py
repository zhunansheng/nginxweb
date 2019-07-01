from __future__ import absolute_import, unicode_literals
import functools
from django.http import HttpResponse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from .models import (
    grained
)


def grained_permissions(func):
    '''

    :argument 装饰器函数,校验细化权限。非法请求直接返回401交由前端判断状态码

    '''
    @functools.wraps(func)
    def wrapper(self, request, args=None):
        if request.method == "PUT" and args != 'connection':
            return func(self, request, args)
        else:
            if request.method == "GET":
                permissions_type = request.GET.get('permissions_type')
            else:
                permissions_type = request.data['permissions_type']
            user = grained.objects.filter(username=request.user).first()
            # if user is not None and user.permissions[permissions_type] == '1':
            if user is not None:
                return func(self, request, args)
            else:
                return HttpResponse(status=401)
    return wrapper



