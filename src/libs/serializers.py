'''
serializers 
'''
from rest_framework import serializers
from core.models import Usermessage,Account

from core.models import SqlDictionary




class MessagesUser(serializers.HyperlinkedModelSerializer):
    '''
    站内信列表serializers
    '''
    class Meta:
        model = Usermessage
        fields = ('title', 'time')


class UserINFO(serializers.HyperlinkedModelSerializer):
    '''
    平台用户信息列表serializers
    '''
    class Meta:
        model = Account
        fields = ('id','username', 'group', 'department', 'email', 'role')





