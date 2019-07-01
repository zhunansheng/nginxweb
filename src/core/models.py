'''
 Create your models here.

'''
from django.db import models
from django.contrib.auth.models import AbstractUser
import ast
from datetime import datetime


Task_Status = (
        (0, "开始"),
        (1, "结束"),
        (2, "出错")
)

Resource_type = (
        ('ldapuser', "ldap用户管理"),
        ('ldapvirtualgroup', "ldap虚拟组"),
        ('nginx', "nginx")
)
class JSONField(models.TextField):
    description = "Json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if not value:
            value = {}
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_save(value)


class Account(AbstractUser):
    '''
    User table
    '''
    group = models.CharField(max_length=40)   #权限组 guest/admin
    department = models.CharField(max_length=40) #部门
    role = models.CharField(max_length=40, null=True)
    name = models.CharField(max_length=40, null=True,verbose_name="名字")
    nickname = models.CharField(max_length=40, null=True, verbose_name="真名")


class SqlDictionary(models.Model):   
    '''
    数据库字典表
    '''
    BaseName = models.CharField(max_length=100)  #库名
    TableName = models.CharField(max_length=100) #表名
    Field = models.CharField(max_length=100) #字段名
    Type = models.CharField(max_length=100) #类型
    Extra = models.TextField() #备注
    TableComment = models.CharField(max_length=100) #表备注
    Name = models.CharField(max_length=100, null=True) #连接名

    def __str__(self):
        return self.TableName





class Todolist(models.Model):
    '''
    todo info 
    '''
    username = models.CharField(max_length=50) #账户
    content = models.CharField(max_length=200) #内容


class Usermessage(models.Model):
    '''
    user  message
    '''
    to_user = models.CharField(max_length=50) #收信人
    from_user = models.CharField(max_length=50) #发件人
    content = models.TextField(max_length=500) #内容
    time = models.CharField(max_length=50) #发送时间
    state = models.CharField(max_length=10) #发送状态
    title = models.CharField(max_length=100) # 站内信标题




class globalpermissions(models.Model):
    '''

    globalpermissions

    '''
    authorization = models.CharField(max_length=50, null=True, db_index=True)
    dingding = models.SmallIntegerField(default=0)
    email = models.SmallIntegerField(default=0)


class grained(models.Model):
    username = models.CharField(max_length=50,db_index=True)
    permissions = JSONField()





class nginxinfo(models.Model):
    '''
      nginx配置信息
    '''
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,unique=True, verbose_name="名称，用来渲染配置文件名")
    listen = models.CharField(max_length=200, verbose_name="监听端口")
    server_name = models.CharField(max_length=200, verbose_name="监听的域名")
    staticpath = models.CharField(max_length=200, null=True,blank=True,default='',verbose_name="静态文件地址")
    defaultpage = models.CharField(max_length=200,null=True,blank=True,default='', verbose_name="默认页面")
    access_log = models.CharField(max_length=200, null=True,blank=True,default='',verbose_name="访问日志")
    error_log = models.CharField(max_length=200,null=True,blank=True,default='', verbose_name="错误日志")
    single = models.BooleanField(default=False,verbose_name="启用节点HTTP状态检测")
    othervalue = models.CharField(max_length=200, null=True,blank=True,default='',verbose_name="其它参数")
    remark = models.CharField(max_length=200,null=True,blank=True, verbose_name="备注")
    locationdata = models.TextField(null=True,blank=True,default='',verbose_name='正则匹配规则')
    defaulthealth = models.BooleanField(verbose_name="使用默认健康页")
    otherhealthpage = models.CharField(max_length=200,null=True,blank=True,default='', verbose_name="使用其它健康页")
    mod_date = models.DateTimeField('最后修改日期',auto_now=True,null=True,blank=True,)
    user = models.ForeignKey(Account, verbose_name="提交人员", null=True,blank=True,related_name="nginxinfo_account",on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True,null=True,blank=True,verbose_name="创建时间")








