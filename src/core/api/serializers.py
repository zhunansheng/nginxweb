# -*- coding: utf-8 -*-
__author__ = 'nanfeng'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models import nginxinfo



class NginxInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    commit_user = serializers.CharField(source='user.name',read_only=True)
    mod_date= serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = nginxinfo
        validators = [
            UniqueTogetherValidator(
                queryset=nginxinfo.objects.all(),
                fields=('server_name', 'listen'),
                message='访问的域名和服务端口不允许重复，请修改后再提交'
            )
        ]
        fields = "__all__"

















