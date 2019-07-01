
#coding: utf-8
from jinja2 import PackageLoader,Environment,FileSystemLoader
import jinja2
def nginxrender(value):
    print(value)
    RENDER_RULES_TEMPLATE = """{%- for up in proxy.upstreamlist %}
upstream {{ up.upnodename }} {
  {{ up.upvalue }}
}
{%- endfor %}
server {
    listen {{ proxy.listen }};
    {%- if proxy.server_name != '' %}
    server_name {{ proxy.server_name }};
    {%- endif %}
    {%- if proxy.error_log %}
    error_log {{ proxy.error_log }};
    {%- endif %}
    {%- if proxy.access_log %}
    access_log {{ proxy.access_log }};
    {%- endif %}
    {%- if proxy.defaultpage != '' %}
    index {{ proxy.defaultpage }};
    {%- endif %}
    {%- if proxy.staticpath != '' %}
    root {{ proxy.staticpath }};
    {%- endif %}
    {%- if proxy.othervalue != '' %}
    {{ proxy.othervalue }}
    {%- endif %}
    {%- if proxy.defaulthealth %}
    location /static/ok.htm {
       root html;
    }
    {%- endif %}
    {%- if proxy.otherhealthpage != '' %}
    {{ proxy.otherhealthpage }}
    {%- endif %}
    {%- for reg in proxy.regurllist %}
    location {{ reg.regurl }} {
        {%- if reg.single %}
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_buffering off;
        {%- endif %}
        {%- if reg.regproxy_address != '' %}
        proxy_pass {{ reg.regproxy_address }};
        {%- endif %}
        {%- if reg.otherparameter != '' %}
        {{ reg.otherparameter }}
        {%- endif %}
    }
    {%- endfor %}
}

    """
    result = jinja2.Template(source=RENDER_RULES_TEMPLATE).render(proxy=value)
    return result
