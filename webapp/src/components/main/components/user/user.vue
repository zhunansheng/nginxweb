<template>
  <div class="user-avatar-dropdown">
    <Dropdown @on-click="handleClick">
      {{ name }}
      <Icon :size="18" type="md-arrow-dropdown"></Icon>
      <DropdownMenu slot="list">
        <DropdownItem name="message">
          消息中心<Badge style="margin-left: 10px" :count="messageUnreadCount"></Badge>
        </DropdownItem>
        <DropdownItem name="logout">退出登录</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  </div>
</template>

<script>
import './user.less'
// eslint-disable-next-line
/* eslint-disable */
import { mapActions } from 'vuex'
import Cookies from 'js-cookie'
export default {
  name: 'User',
  data () {
            return {
              name: Cookies.get('name')
            }
        },
  props: {
    userAvatar: {
      type: String,
      default: ''
    },
    messageUnreadCount: {
      type: Number,
      default: 0
    }
  },
  methods: {
    ...mapActions([
      'handleLogOut'
    ]),
    logout () {
        Cookies.remove('user');
        Cookies.remove('password');
        Cookies.remove('hasGreet');
        Cookies.remove('access');
        Cookies.remove('yduss_production_m_v2',{domain:'.hipac.cn'});
        Cookies.remove('yduss_production_m_v2',{domain:'.yangtuojia.com'});
        Cookies.set('yduss_production_m_v2', '0', { expires: -1 });
        localStorage.clear('yduss_production_m_v2')
        this.$router.push({
          name: 'login'
        });
    },
    message () {
      this.$router.push({
        name: 'message_page'
      })
    },
    handleClick (name) {
      switch (name) {
        case 'logout': this.logout()
          break
        case 'message': this.message()
          break
      }
    }
  }
}
</script>
