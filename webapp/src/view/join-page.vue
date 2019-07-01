<template>
  <div>
    <Card shadow title="帮助">
      <h2>nginx负载均衡管理说明</h2>
      <br>
     <p>1、渲染nginx配置</p>
<p>2、保存配置入库</p>
<p>3、重新编辑原配置</p>
<p>4、提供直接管理文件方式，不走模版渲染，兼容线上已有的配置文件</p>
<p>5、考虑到各位小伙伴需求不一致，也没有托管防火墙，所以留下很大扩展空间给各位接入其它系统</p>
    </Card>
  </div>
</template>

<script>
export default {
  name: 'join_page',
  data () {
    return {
    }
  }
}
</script>
<style>
  .join-page{
    text-align: center;
  }
  .qq-group-img{
    width: 100%;
  }
  .join-page-other-icon{
    width: 20px;
    vertical-align: middle;
    margin-right: 6px;
  }
  .join-page-other{
    text-align: left;
  }
  .join-page-other .ivu-btn{
    margin-right: 6px;
  }
</style>
