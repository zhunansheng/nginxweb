from libs import baseview
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import (
    Usermessage,
    Account,
    Todolist,
    grained
)
from libs.serializers import (
    UserINFO,
    MessagesUser
)




class dashboard(baseview.BaseView):

    '''

    :argument 主页面展示数据接口api

    get  主页图表信息

    put todo列表 删除todo 个人信息

    post todo提交

    '''

    def put(self, request, args=None):

        if args == 'todolist':
            try:
                user = request.data['username']
            except KeyError as e:
                return HttpResponse(status=500)
            else:
                try:
                    todo = Todolist.objects.filter(username=user).all()
                    return Response([{'title': i.content} for i in todo])
                except Exception as e:
                    return HttpResponse(status=500)

        elif args == 'deltodo':
            try:
                user = request.data['username']
                todo = request.data['todo']
            except KeyError as e:
                return HttpResponse(status=500)
            else:
                try:
                    Todolist.objects.filter(username=user, content=todo).delete()
                    return Response('')
                except Exception as e:
                    return HttpResponse(status=500)

        elif args == 'ownspace':
            user = request.data['user']
            info = Account.objects.filter(username=user).get()
            _serializers = UserINFO(info)
            permissions = grained.objects.filter(username=request.user).first()
            return Response({'userinfo':_serializers.data, 'permissons': permissions.permissions})

        elif args == 'statement':
            Account.objects.filter(username=request.user).update(last_name='1')
            return Response('')

    def post(self, request, args=None):
        try:
            user = request.data['username']
            todo = request.data['todo']
        except Exception as e:
            return HttpResponse(status=500)
        else:
            try:
                Todolist.objects.get_or_create(username=user, content=todo)
                return Response('')
            except Exception as e:
                return HttpResponse(status=500)


class messages(baseview.BaseView):
    '''

    :argument 站内信功能相关接口api

    :get  站内信列表

    :put  站内信详细内容

    :post 更新站内信状态

    :del 删除站内信

    '''

    def get(self, request, args=None):
        try:
            unread = Usermessage.objects.filter(
                state='unread',
                to_user=args
                ).all().order_by('-time')
            serializers_unread = MessagesUser(unread, many=True)
            read = Usermessage.objects.filter(
                state='read',
                to_user=args
                ).all().order_by('-time')
            serializers_read = MessagesUser(read, many=True)
            recovery = Usermessage.objects.filter(
                state='recovery',
                to_user=args
                ).all().order_by('-time')
            serializers_recovery = MessagesUser(recovery, many=True)
            data = {'unread': serializers_unread.data, 'read': serializers_read.data,
                    'recovery': serializers_recovery.data}
            return Response(data)
        except Exception as e:
            return HttpResponse(status=500)

    def put(self, request, args=None):
        try:
            title = request.data['title']
            time = request.data['time']
        except KeyError as e:
            return HttpResponse(status=500)
        else:
            try:
                data = Usermessage.objects.filter(to_user=args, title=title, time=time).get()
                return Response({'content': data.content, 'from_user': data.from_user})
            except Exception as e:
                return HttpResponse(status=500)

    def post(self, request, args=None):
        try:
            title = request.data['title']
            time = request.data['time']
            state = request.data['state']
        except KeyError as e:
            return HttpResponse(status=500)
        else:
            try:
                Usermessage.objects.filter(
                    to_user=str(args).rstrip('/'),
                    title=title,
                    time=time
                    ).update(state=state)
                return Response('')
            except Exception as e:
                return HttpResponse(status=500)

    def delete(self, request, args=None):
        try:
            data = str(args).split('_')
            Usermessage.objects.filter(
                to_user=data[0],
                title=data[1],
                time=data[2]
                ).update(state='recovery')
            return Response('')
        except Exception as e:
            return HttpResponse(status=500)


