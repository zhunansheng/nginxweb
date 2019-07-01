# nginxweb
<h1>
nginx负载均衡管理器
    <h3>基于django rest framework和iview admin iView.</h3>
</h1>

## 功能

- 登录 / 退出
- 基于模版的渲染
    - 支持upstream
    - location
- i18n（国际语言）
- 组件
    - iview admin
    - dango rest framework
    - vue
    - python3
    - jinja2
## 基础组件安装
```bush
#  node和npm安装
wget https://npm.taobao.org/mirrors/node/v10.14.1/node-v10.14.1-linux-x64.tar.gz
tar -xvf  node-v8.0.0-linux-x64.tar.xz
mv node-v8.1.4-linux-x64 node

# 配置环境变量
vim /etc/profile
#set for nodejs  
export NODE_HOME=/usr/local/node  
export PATH=$NODE_HOME/bin:$PATH

#生效配置文件
source /etc/profile
node -v
npm -v

#后端组件安装
$ yum update -y

# 防火墙 与 selinux 设置说明, 如果已经关闭了 防火墙 和 Selinux 的用户请跳过设置
$ systemctl start firewalld
$ firewall-cmd --zone=public --add-port=80/tcp --permanent  # nginx 端口
$ firewall-cmd --zone=public --add-port=2222/tcp --permanent  # 用户SSH登录端口 koko
  --permanent  永久生效, 没有此参数重启后失效

$ firewall-cmd --reload  # 重新载入规则

$ setenforce 0
$ sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config

# 安装依赖包
$ yum -y install wget gcc epel-release git

# 安装 Redis, Jumpserver 使用 Redis 做 cache 和 celery broke
$ yum -y install redis
$ systemctl enable redis
$ systemctl start redis

# 安装 MySQL
$ yum -y install mariadb mariadb-devel mariadb-server MariaDB-shared # centos7下叫mariadb, 用法与mysql一致
$ systemctl enable mariadb
$ systemctl start mariadb

# 安装 Nginx, 可以用来代理生成的静态文件
$ vi /etc/yum.repos.d/nginx.repo

[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/7/$basearch/
gpgcheck=0
enabled=1

$ yum -y install nginx
$ systemctl enable nginx

# 安装 Python3.6
$ yum -y install python36 python36-devel

# 配置并载入 Python3 虚拟环境
$ cd /opt
$ python3.6 -m venv py3  # py3 为虚拟环境名称, 可自定义
$ source /opt/py3/bin/activate  # 退出虚拟环境可以使用 deactivate 命令

```

## 运行项目
```bush
# clone the project
git clone git@github.com:zhunansheng/nginx_balance.git

//进入前端目录
cd webapp

// 安装依赖
npm install

//修改webapp里的接口地址，改成自己的后端接口
webapp/view/components/api/api.js

//进入后端目录
cd src


// 安装依赖
pip install -r requirements.txt



// 直接运行前端
npm run dev
```

## 生成静态文件，会自动创建dist文件，nginx可配置到此目录
```bush
npm run build
```
