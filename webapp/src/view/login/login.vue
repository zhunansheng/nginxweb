<style>
/* .div-relative {
  position: relative;
  width: 100%;
}

.div-a {
  position: absolute;
  left: 38%;
  top: 20%;
  width: 350px;
  height: 100px
} */
</style>

<style lang="less">
  @import './login.less';
</style>

<template>
  <div class="login">
    <div class="login-con">
      <Card icon="log-in" title="欢迎登录" :bordered="false">
        <div class="form-con">
          <login-form @on-success-valid="handleSubmit"></login-form>
          <p class="login-tip">帐号和密码都是admin</p>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
// eslint-disable-next-line
/* eslint-disable */
import { login } from '../components/api/api.js'
import Cookies from 'js-cookie'
import axios from 'axios'
import LoginForm from '_c/login-form'
import { mapActions } from 'vuex'
export default {
  components: {
    LoginForm
  },
  methods: {
    ...mapActions([
      'handleLogin',
      'getUserInfo'
    ]),
    handleSubmit ({ userName, password }) {
      this.handleLogin({ userName, password }).then(res => {
        this.getUserInfo().then(res => {
          this.$router.push({
            name: this.$config.homeName
          })
        })
      })
    }
  },
  mounted () {
  }
}
</script>

<style>

</style>
