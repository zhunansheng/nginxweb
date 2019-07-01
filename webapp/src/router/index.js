// eslint-disable-next-line
/* eslint-disable */
import Vue from 'vue'
import Router from 'vue-router'
import routes from './routers'
import store from '@/store'
import iView from 'iview'
import { getToken, canTurnTo, setTitle } from '@/libs/util'
import config from '@/config'
const { homeName } = config

Vue.use(Router)
const router = new Router({
  routes,
  mode: 'hash'
})
const LOGIN_PAGE_NAME = 'login'

router.beforeEach((to, from, next) => {
  iView.LoadingBar.start()
  console.log(to.name)
  const token = getToken()
  console.log(token)
  if (!token && to.name === LOGIN_PAGE_NAME) {
    next()
    iView.LoadingBar.finish()
  } else if (!token && to.name !== LOGIN_PAGE_NAME) {
    next({name: LOGIN_PAGE_NAME})
    iView.LoadingBar.finish()
  }
  else {
    next()
    iView.LoadingBar.finish()
  }
})

router.afterEach(to => {
  iView.LoadingBar.finish()
  window.scrollTo(0, 0)
})

export default router
