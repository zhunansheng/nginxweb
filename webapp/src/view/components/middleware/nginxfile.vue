/* eslint-disable */
// eslint-disable-next-line
<template>
  <div>
    <Row>
      <Col span="24">
        <Card>
          <p slot="title">
            <Icon type="ios-redo"></Icon>
            负载均衡
          </p>
          <Row>
            <Form ref="formInline"  inline>
              <FormItem>
                <p>主机选择</p>
                </FormItem>
              <FormItem>
            <Select v-model="hostvalue" filterable style="width:150px" @on-change="hostchange">
                    <Option v-for="i in hostchoicelist" :key="i.value" :value="i.value" >{{ i.label }}</Option>
            </Select>
            </FormItem>
            <FormItem>
              <Button type="primary" style="float: right;">
              刷新
            </Button>
            </FormItem>
            </Form>
          </Row>
              <Row>
                  <Table :columns="tablecolumns" :data="data6"></Table>
              </Row>
              <br>
              <Page :total="pagenumber" show-elevator @on-change="currentpage" :page-size="15"></Page>
        </Card>
      </Col>
      <Modal v-model="moda0" width="500">
  <Card>
    <p slot="title">
      <Icon type="load-b"></Icon>
      添加分组
    </p>
    <div class="edittable-testauto-con">
      <Form :model="formValidate" :label-width="80" ref="formValidate" :rules="ruleValidate">
        <FormItem label="名称" prop="name">
          <Input v-model="formValidate.host_groupname" placeholder="请输入"></Input>
        </FormItem>
        <FormItem label="规则内容" prop="desc">
          <Input v-model="formValidate.host_groupdesc" placeholder="请输入"></Input>
        </FormItem>
      </Form>
    </div>
  </Card>
  <div slot="footer">
        <Button type="primary" @click.native="groupsave" style="margin-left: 35%">保存</Button>
      </div>
  </Modal>
  <Modal v-model="moda1" width="1200">
  <Card>
    <p slot="title">
      <Icon type="load-b"></Icon>
      创建负载均衡
    </p>
    <Row>
      <Col span="14">
    <Tabs value="name1">
        <TabPane label="基础配置" name="name1">
          <div class="edittable-testauto-con">
      <Form :model="formValidate" :label-width="120" ref="formValidate" :rules="ruleValidate">
        <FormItem label="名称:">
              <Input v-model="formValidate.title" placeholder="用来描述负载均衡器"></Input>
        </FormItem>
         <FormItem label="服务端口:">
              <Input v-model="formValidate.listen" placeholder="负载均衡器对外提供服务端口"></Input>
        </FormItem>
        <FormItem label="访问域名:">
              <Input v-model="formValidate.server_name" placeholder="监听的域名(多个空格分开)"></Input>
        </FormItem>
        <FormItem label="静态文件所在路径:">
              <Input v-model="formValidate.staticpath" placeholder="比如/alidata/file"></Input>
        </FormItem>
        <FormItem label="默认页面:">
              <Input v-model="formValidate.defaultpage" placeholder="根url默认页面，比如index.html 多个以空格隔开"></Input>
        </FormItem>
        <FormItem label="访问日志:">
              <Input v-model="formValidate.access_log" placeholder="访问日志路径"></Input>
        </FormItem>
        <FormItem label="错误日志:">
              <Input v-model="formValidate.error_log" placeholder="错误日志路径"></Input>
        </FormItem>
        <FormItem label="其它参数:">
              <Input v-model="formValidate.othervalue" type="textarea" :rows="3" placeholder="自定义一些参数，如more_clear_headers 'X-Current-Location';"></Input>
        </FormItem>
         <FormItem label="HTTP检测:">
              <Checkbox v-model="single">启用节点HTTP状态检测</Checkbox>
        </FormItem>
        <FormItem label="备注">
              <Input v-model="formValidate.remark" placeholder="请输入"></Input>
        </FormItem>
        <FormItem label="目标主机:">
              <Select v-model="formValidate.targetlist"  multiple style="width:200px">
                <Option v-for="item in ecsList" :value="item.value" :key="item.value">{{ item.label }}</Option>
              </Select>
        </FormItem>
        <br>
        <br>
      </Form>
    </div>
        </TabPane>
        <TabPane label="匹配规则" name="name2">
           <Form :model="regValidate" :label-width="120" ref="regValidate" :rules="ruleValidate">
        <FormItem label="匹配的url:">
              <Input v-model="regValidate.regurl" placeholder="如 ^~ /pc-doc/"></Input>
        </FormItem>
        <FormItem label="添加默认参数:">
              <Checkbox v-model="regValidate.single"></Checkbox>
              <p>勾选将自动追加以下参数</p>
              <p>proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-Server $host;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;</p>
        </FormItem>
        <FormItem label="反向代理地址:">
              <Input v-model="regValidate.regproxy_address" placeholder="如http://site-js-pro.oss-cn-hangzhou-internal.aliyuncs.com/uc/; "></Input>
        </FormItem>
        <FormItem label="其它参数:">
              <Input v-model="regValidate.otherparameter"  type="textarea" :rows="3" placeholder="如rewrite ^(.*)$ /system-asset/fed-pp/pp-admin-static/prod/index.html break;"></Input>
        </FormItem>
        <FormItem>
            <Button type="primary" @click="addregex">增加</Button>
        </FormItem>
      </Form>
     <Row>
                  <Table border :columns="columns1" :data="locationdata" stripe size="small" @on-selection-change="handleSelection"></Table>
              </Row>
        </TabPane>
        <TabPane label="健康页" name="name3">
          <Form :model="formValidate" :label-width="120" ref="formValidate" :rules="ruleValidate">
        <FormItem label="使用默认健康页:">
              <Checkbox v-model="formValidate.defaulthealth"></Checkbox>
              <p>勾选将自动使用下面健康页</p>
              <p>location /static/ok.htm{
               root html;
                }</p>
        </FormItem>
        <FormItem label="其它参数:" v-show="!formValidate.defaulthealth">
              <Input v-model="formValidate.otherhealthpage" placeholder="如location /static/success.htm{ root html; }"></Input>
        </FormItem>
      </Form>
        </TabPane>
    </Tabs>
    </Col>
    <Col span="9" offset="1">
    <Card>
      <p slot="title">
      <Icon type="load-b"></Icon>
      nginx配置预览
    </p>
    <Input v-model="value6" type="textarea" :rows="20" placeholder="Enter something..." />
    </Card>
    </Col>
    </Row>
  </Card>
  <div slot="footer">
        <Button type="info" @click.native="preview" >预览配置</Button>
        <Button v-show="detail_action" type="primary" @click.native="nginxsave()" >保存</Button>
        <Button v-show="!detail_action" type="primary" @click.native="nginxsave()" >更新配置</Button>
        <Button type="success" @click.native="nginxcheck()" >测试</Button>
        <Button type="success" @click.native="nginxcheck()" >执行</Button>
      </div>
  </Modal>
  <Modal v-model="moda2" width="260">
    <Checkbox v-model="deletefile">同时删除目标服务器上的文件</Checkbox>
  </Modal>
  <Modal v-model="nginxtestmodel" width="400">
    <p v-html="nginxtestdata"></p>
  </Modal>
  <Modal v-model="moda3" width="700">
    <Card>
      <p slot="title">
      nginx配置预览
    </p>
    <Input v-model="filecontent" type="textarea" :rows="25" placeholder="内容读取中....." />
    </Card>
    <div slot="footer">
        <Button type="info" @click.native="preview" >测试</Button>
        <Button  type="primary" @click.native="nginxfilesaveinfo()" >保存</Button>
        <Button  type="primary" @click.native="nginxreloadinfo()" >nginx重载</Button>
      </div>
  </Modal>
    </Row>
  </div>
</template>
<script>
/* eslint-disable */
// eslint-disable-next-line
import Cookies from 'js-cookie'
import { quillEditor } from 'vue-quill-editor'
import { nginxinfo } from '../api/api.js'
import { addnginxsave } from '../api/api.js'
import { gettargethost } from '../api/api.js'
import { nginxcheck, nginxreaddir, nginxfileread, nginxfilesave, nginxreload, nginxfiledelte } from '../api/api.js'
import util from '../../../libs/util'
import { previewproperties } from '../api/api.js'
import axios from 'axios'
    export default {
      components: {
      quillEditor
    },
      data () {
        return {
        moda0: false,
        moda1: false,
        detail_action: true,
        moda3: false,
        ecsList: [],
        modifytime: '',
        nginxtestmodel: false,
        filecontent: '',
        deletefile: true,
        filename: '',
        nginxtestdata: '后端正在检测中.....',
        moda2: false,
              formValidate: {
                defaulthealth: false,
                targetlist: [],
                otherhealthpage: '',
                staticpath: '',
                otherparameter: '',
                server_name: '',
                defaultpage: '',
                access_log: '',
                error_log: '',
                othervalue: ''
              },
              loading: true,
              regValidate: {},
              detail: true,
              value6: '',
              typechosevalue: '',
              hostchoicelist: [
                {
                  label: 'cmdb',
                  value: 'cmdb'
                }
              ],
              data: [],
              data6: [],
              searchConName: '',
              cancelreason: '',
              locationdata: [],
              pagenumber: '',
              selectordernumber: '',
              methodsvalue: '',
              discussform: {},
              file: [],
           typevalue: '',
           create_time: '',
           content: '123',
        columns2: [
                    {
                        title: 'Name',
                        key: 'name'
                    },
                    {
                        title: 'Age',
                        key: 'age'
                    },
                    {
                        title: 'Address',
                        key: 'address'
                    }
                ],
            columns1: [
           {
            type: 'selection',
            width: 60,
            align: 'center'
          },
          {
            title: '匹配的url',
            align: 'center',
            width: '120',
            key: 'regurl'
          },
          {
            title: '反向代理地址',
            key: 'regproxy_address'
          },
          {
            title: '其它参数',
            key: 'otherparameter'
          },
          {
            title: '添加默认参数',
            key: 'single',
            rrender: (h, params) => {
              const row = params.row
              let text = ''
              let color = ''
              if (single) {
                text = '是'
                color = 'green'
              } else {
                text = '否'
                color = 'red'
              }
              return h('span', {
                style: {
                  color: color
                }
              }, text)
            }
          },
          {
            title: '操作',
            key: 'action',
            width: 150,
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    size: 'small',
                    type: 'error'
                  },
                  style: {
                    marginLeft: '5px'
                  },
                  on: {
                    click: () => {
                      this.del_tab(params.row)
                    }
                  }
                }, '删除')
              ])
            }
          }
        ],
        tablecolumns: [
          {
            title: '文件名',
            align: 'center',
            key: 'filename'
          },
          {
            title: '占用空间(b)',
            align: 'center',
            key: 'size'
          },
          {
            title: '权限',
            align: 'center',
            key: 'access'
          },
          {
            title: '用户',
            align: 'center',
            key: 'user'
          },
          {
            title: '类型',
            align: 'center',
            key: 'file_type'
          },
          {
            title: '日期',
            align: 'center',
            key: 'date'
          },
          {
            title: '最后修改时间',
            align: 'center',
            key: 'modifytime'
          },
          {
            title: '操作',
            key: 'action',
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    size: 'small',
                    type: 'info'
                  },
                  style: {
                    marginLeft: '5px'
                  },
                  on: {
                    click: () => {
                      this.detail_file(params.row)
                    }
                  }
                }, '编辑'),
                h('Poptip', {
          style:{
            textAlign: 'left',
            marginLeft: '5px'
          },
          props: {
            placement:'left-start',
            confirm: true,
            title: '确定删除吗？',
          },
          on: {
            // 必须是箭头函数写法
            'on-ok': ()=> {
              //调用删除方法
              this.remove(params.row)
                console.log('删除')
            },
            'on-cancel': ()=> {
                console.log('取消')
            }
          }
        },[
          h('Button', {
            props: {
              type: 'error',
              size: 'small'
            },
            on: {
              click: () => {
                //this.remove(params.index)
              }
            }
          }, '删除')
        ])
              ])
            }
          }
        ],
            copyuser: []
            }
        },
        methods: {
          remove (row) {
            nginxfiledelte({
              'filename': row.filename,
              'host': this.hostvalue,
              'modifytime': row.modifytime
            }).then(res => {
              console.log(res)
            })
          },
          nginxreloadinfo () {
            this.$Loading.start();
            nginxreload({
              'host': this.hostvalue
            }).then(res => {
              this.$Loading.finish();
              this.$Message.success('nginx reload成功')
            }).catch(error => {
              this.$Loading.error();
            util.ajanxerrorcode(this, error)
          })
          },
          nginxfilesaveinfo () {
            nginxfilesave({
              'host': this.hostvalue,
              'filename': this.filename,
              'filecontent': this.filecontent,
              'modifytime': this.modifytime
            }).then(res => {
              this.$Message.success('保存成功')
            }).catch(error => {
              this.$Loading.error();
            util.ajanxerrorcode(this, error)
          })
          },
          hostchange () {
            nginxreaddir({
            'host': 'cmdb'
          }).then(res => {
            this.data6 = res.data['results']
          })
          },
          detail_file (row) {
            console.log(row)
            this.$Loading.start();
            this.filecontent = ''
            this.moda3 = true
            this.filename = row.filename
            nginxfileread({
            'host': this.hostvalue,
            'filename': row.filename
          }).then(res => {
            this.filecontent = res.data['results']
            this.modifytime = res.data['modifytime']
            this.$Loading.finish();
          }).catch(error => {
            this.$Loading.error();
            util.ajanxerrorcode(this, error)
          })
          },
          nginxcheck () {
            this.nginxtestdata = '后端正在检测中.....'
            console.log(this.formValidate.targetlist)
            if (this.formValidate.targetlist.length === 0) {
              this.$Message.error('目标主机不能为空')
            } else {
              this.formValidate['regurllist'] = this.locationdata
              this.nginxtestmodel = true
              nginxcheck({
                'hostlist': this.formValidate.targetlist,
                'title': this.formValidate.title,
                'nginxinfo': this.formValidate
              }).then(res => {
                this.nginxtestdata = res.data
              }).catch(error => {
            util.ajanxerrorcode(this, error)
          })
            }
          },
          del_balance (row) {
            this.moda2 = true
          },
          clone_nginx (row) {
            this.detail_action = true
            this.formValidate = row
            this.locationdata = JSON.parse(row['locationdata'])
            this.moda1 = true
          },
          detail_nginx (row) {
            this.detail_action = false
            this.formValidate = row
            this.locationdata = JSON.parse(row['locationdata'])
            this.moda1 = true
          },
          addregex () {
        let tempdict = {}
        tempdict['regurl'] = this.regValidate.regurl
        tempdict['regproxy_address'] = this.regValidate.regproxy_address
        tempdict['single'] = this.regValidate.single
        tempdict['otherparameter'] = this.regValidate.otherparameter
        this.locationdata.push(tempdict)
      },
          nginxsave () {
            this.formValidate['locationdata'] = JSON.stringify(this.locationdata)
            addnginxsave(this.formValidate).then(res => {
              this.$Message.success('保存成功')
              this.moda1 = false
              nginxinfo().then(res => {
              this.data6 = res.data['results']
            })
            }).catch(error => {
            util.ajanxerrorcode(this, error)
          })
          },
          preview () {
        console.log(JSON.stringify(this.locationdata))
        this.formValidate['regurllist'] = this.locationdata
        previewproperties(
          this.formValidate).then(res => {
            this.value6 = res.data
          })
      },
          createbalance () {
            gettargethost().then(res => {
              this.ecsList = res.data
            })
            this.detail_action = true
        this.moda1 = true
      },
          del_tab (row) {
        console.log(row['_index'])
        this.locationdata.splice(row['_index'],1)
      },
      edit_tab (row) {
        console.log(row['_index'])
        this.locationdata.splice(row['_index'],1)
      },
          typechange () {
            console.log(this.typechosevalue)
            let params = {}
            params['type'] = this.typechosevalue
            this.get_myorder(params)
          },
          get_myorder (params) {
            myordersearch(params).then(res => {
            this.data = res.data['results']
            this.pagenumber = res.data['count']['alter_number']
            this.loading = false
          })
          },
          reload () {
            this.get_myorder()
            this.$Notice.success({
              title: '刷新成功'
            })
          },
          clearcheck () {
            this.searchConName = ''
            myordersearch().then(res => {
            this.data = res.data['results']
            this.pagenumber = res.data['count']['alter_number']
            this.loading = false
          })
          },
          handleSearch () {
            myordersearch({
              'search': this.searchConName
            }).then(res => {
            this.data = res.data['results']
            console.log(this.data)
            this.pagenumber = res.data['count']['alter_number']
            this.loading = false
          })
          },
          cancelsave () {
            ordercancel({
              'id': this.orderid,
              'cancelreason': this.cancelreason
            }).then(res => {
              this.$Notice.success({
              title: '撤销成功'
            })
            this.get_myorder()
            })
         },
          commitdiscuss () {
        adddiscuss({
          'ordernumber': this.ordernumber,
          'content': this.discussform.content
        }).then(res => {
          this.$Notice.success({
              title: '评论成功'
            })
          discuss({
          'ordernumber': this.ordernumber
        }).then(res => {
          this.discussdata = res.data
        })
        })
      },
          cancel_button (orderid) {
            //缓存选择了哪一行
          this.orderid = orderid
          this.reject.reje = true
      },
          order_return () {
        this.detail = true
        console.log('true')
      },
      currentpage (vl) {
        myordersearch({
          'page': vl
        }).then(res => {
            this.data = res.data['results']
            this.pagenumber = res.data['count']
            this.loading = false
          })
      }
        },
        mounted () {
        }
    }
</script>
