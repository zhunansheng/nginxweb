'''
url table
'''
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from core.api.nginxview import nginxView,NginxInfoSaveView,TargetHostView,\
    nginx_checkView,NginxFileManager,NginxServiceView


from core.api.user import (
    login_auth
)
from core.api.dashboard import (
    dashboard,
    messages
)



router = DefaultRouter()



#nginx配置保存，删除，修改，查询

router.register(r'api/v1/nginxsave', NginxInfoSaveView)



urlpatterns = [
    url(r'^api/v1/previewproperties/(.*)', nginxView.as_view()),
    #nginx 文件管理管理
    url(r'^api/v1/nginxfilemanager/(.*)', NginxFileManager.as_view()),
    url(r'^api/v1/targethost/(.*)', TargetHostView.as_view()),
    url(r'^api/v1/nginxcheck/(.*)', nginx_checkView.as_view()),
    url(r'^api/v1/nginxcheck/(.*)', nginx_checkView.as_view()),
    url(r'^api/v1/nginxservice/(.*)', NginxServiceView.as_view()),
    url(r'^api/v1/homedata/(.*)', dashboard.as_view()),
    url(r'^api/v1/messages/(.*)', messages.as_view()),
    url(r'^api-token-auth', login_auth.as_view()),
    url(r'^', include(router.urls)),
]

