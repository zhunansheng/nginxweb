#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'nanfeng'
import requests
import json
import re
try:
    import cookielib
except:
    import http.cookiejar as cookielib

# 使用urllib2请求https出错，做的设置
import ssl
context = ssl._create_unverified_context()

# 使用requests请求https出现警告，做的设置
#from salt_settings import salt_api_url, salt_api_pass, salt_api_user
from core.api.salt_settings import salt_api_url, salt_api_user,salt_api_pass

class SaltApi:
    """
    定义salt api接口的类
    初始化获得token
    """
    def __init__(self, url):
        self.url = salt_api_url
        self.username = salt_api_user
        self.password = salt_api_pass
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
            # "Content-type": "application/x-yaml"
        }
        self.params = {'client': 'local', 'fun': '', 'tgt': ''}
        # self.params = {'client': 'local', 'fun': '', 'tgt': '', 'arg': ''}
        self.login_url = self.url + "login"
        self.login_params = {'username': self.username, 'password': self.password, 'eauth': 'pam'}
        print(self.get_data(self.login_url, self.login_params))
        self.token = self.get_data(self.login_url, self.login_params)['token']
        self.headers['X-Auth-Token'] = self.token

    def get_data(self, url, params):
        send_data = json.dumps(params)
        print(send_data)
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        # response = request.text
        # response = eval(response)     使用x-yaml格式时使用这个命令把回应的内容转换成字典
        # print response
        # print request
        # print type(request)
        response = request.json()
        result = dict(response)
        # print result
        return result['return'][0]

    def salt_command(self, tgt, method, arg=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'"""
        if arg:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt}
        print('命令参数: ', params)
        result = self.get_data(self.url, params)
        return result

    def salt_async_command(self, tgt, method, arg=None):  # 异步执行salt命令，根据jid查看执行结果
        """远程异步执行命令"""
        if arg:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt}
        jid = self.get_data(self.url, params)['jid']
        return jid

    def look_jid(self, jid):  # 根据异步执行命令返回的jid查看事件结果
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        print(params)
        result = self.get_data(self.url, params)
        return result

def sync(tgt,fun,args):
    print('==================')
    print('同步执行命令')
    salt = SaltApi(salt_api_url)
    print(salt.token)
    salt_client = tgt
    salt_method = fun
    salt_params = args
    # 下面只是为了打印结果好看点
    result1 = salt.salt_command(salt_client, salt_method,salt_params)
    print(result1)
    return result1

def resync():
    print('==================')
    print('异步执行命令')
    salt1 = SaltApi(salt_api_url)
    salt_client = '*'
    salt_method = 'cmd.run'
    salt_params = 'ls'
    # 下面只是为了打印结果好看点

    jid2 = salt1.salt_async_command(salt_client, salt_method, salt_params)
    result2 = salt1.look_jid(jid2)
    print(result2)
    for i in result2.keys():
        print(result2[i])
