<template>
  <Form ref="loginForm" :model="form" :rules="rules" @keydown.enter.native="handleSubmit">
    <FormItem prop="userName">
      <Input v-model="form.userName" placeholder="请输入用户名">
        <span slot="prepend">
          <Icon :size="16" type="ios-person"></Icon>
        </span>
      </Input>
    </FormItem>
    <FormItem prop="password">
      <Input type="password" v-model="form.password" placeholder="请输入密码">
        <span slot="prepend">
          <Icon :size="14" type="md-lock"></Icon>
        </span>
      </Input>
    </FormItem>
    <FormItem>
      <Button @click="handleSubmit" type="primary" long>登录</Button>
    </FormItem>
  </Form>
</template>
<script>
// eslint-disable-next-line
/* eslint-disable */
import { login } from './../../view/components/api/api.js'
import axios from 'axios'
import Cookies from 'js-cookie'
export default {
  name: 'LoginForm',
  props: {
    userNameRules: {
      type: Array,
      default: () => {
        return [
          { required: true, message: '账号不能为空', trigger: 'blur' }
        ]
      }
    },
    passwordRules: {
      type: Array,
      default: () => {
        return [
          { required: true, message: '密码不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  data () {
    return {
      form: {
        userName: 'admin',
        password: ''
      }
    }
  },
  computed: {
    rules () {
      return {
        userName: this.userNameRules,
        password: this.passwordRules
      }
    }
  },
  methods: {
    handleSubmit () {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          login({
        'username': this.form.userName,
        'password': this.form.password
      }
      ).then(res => {
        // debugger
        // console.info(res.data)
        // debugger
            axios.defaults.headers.common['Authorization'] = 'JWT ' + res.data['token']
            Cookies.set('user', res.data['user'])
            Cookies.set('name', res.data['name'])
            Cookies.set('group', res.data['group'])
            console.log(res.data['group'])
            Cookies.set('jwt', 'JWT ' + res.data['token'])
            if (Cookies.get('group') === 'admin') {
               console.log(this.$store)
               this.$store.state.user['access'] ='["admin"]';
               this.$store.commit('Menulist')
            } else {
              this.$store.commit('Menulist');
        //       axios.get(`${util.url}/menu_list`)
        // .then(res => {
            if (localStorage.getItem('pageOpenedList')) {
              localStorage.removeItem('pageOpenedList')
            }
            }
            debugger
            location.href="/"
      }
      )
        }
      })
    }
  }
}
</script>
