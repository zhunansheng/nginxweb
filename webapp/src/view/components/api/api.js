import axios from 'axios'

// eslint-disable-next-line
/* eslint-disable */
let host = 'http://nginxdemo.cmdb.top:9000';
let url = 'http://' + 'nginxdemo.cmdb.top' + ':9000/api/v1'
//登录

export const login = params => {
  return axios.post(`${host}/api-token-auth`, params)
}


//预览nginx配置
export const previewproperties = params => {
  return axios.post(`${url}/nginxservice/preview`, params)
}

// ldap 同步发起
export const ldapresync = params => { return axios.post(`${url}/ldap/resync/`, params) }

// ldap 同步发起
export const delldapuser = params => { return axios.delete(`${url}/ldap/userinfo/` + params + '/') }

// ldap密码比较
export const ldappasswordcheck = params => { return axios.post(`${url}/ldap/passwordcheck/`, params) }

// ldap用户信息查询
export const ldapinfo = params => { return axios.get(`${url}/ldap/userinfo/`, { params: params }) }

// 操作日志
export const operatelog = params => { return axios.get(`${url}/log/operate/`, { params: params }) }


// ldap 用户删除
export const addldapuser = params => { return axios.post(`${url}/ldap/userinfo/`, params) }

// ldap 用户属性更新（密码，用户组）
export const updatedapuser = params => { return axios.put(`${url}/ldap/userinfo/`, params) }

// ldap 虚拟组移除或者增加用户
export const virtualgroupmodifyuser = params => { return axios.post(`${url}/ldap/virtualgroup_modifyuser/`, params) }
// ldap用户信息查询
export const ldapvirtualgroup = params => { return axios.get(`${url}/ldap/virtualgroupinfo/`, { params: params }) }


// 获取运维组用户
export const nginxinfo = params => { return axios.get(`${url}/nginxsave/`, { params: params }) }

//获取目标主机
export const gettargethost = params => { return axios.get(`${url}/targethost/`, { params: params }) }

//获取知人同步信息
export const zhirenresyncinfo = params => { return axios.get(`${url}/zhirenresync/`, { params: params }) }

// 发起知人同步
export const startzhirenresync = params => { return axios.post(`${url}/zhirenresync/`, params) }

// 获取nginx 特定主机目录
export const nginxreaddir = params => { return axios.post(`${url}/nginxfilemanager/readdir`, params) }

// 获取nginx 特定主机文件
export const nginxfileread = params => { return axios.post(`${url}/nginxfilemanager/fileread`, params) }

// 保存nginx 特定主机文件
export const nginxfilesave = params => { return axios.post(`${url}/nginxfilemanager/filesave`, params) }

// 删除nginx 特定文件
export const nginxfiledelte = params => { return axios.post(`${url}/nginxfilemanager/delete`, params) }

nginxcheck
// nginx检测
export const nginxcheck = params => { return axios.post(`${url}/nginxservice/check`, params) }

// nginx重启接口
export const nginxreload = params => { return axios.post(`${url}/nginxservice/reload`, params) }


export const addnginxsave = params => {
  return axios.post(`${url}/nginxsave/`, params)
}
