import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/views/LoginPage.vue'
import StoragePage from '@/views/StoragePage.vue'
import AppConnector from '@/crypto/AppConnector'
import {ConnectionStore} from '@/crypto/helpers'

const routes = [
  {
    path: '/',
    name: 'StoragePage',
    component: StoragePage,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from) => {
  const loginPage = {
    name: 'LoginPage',
    query: {
      need_auth: true,
      redirect: to.fullPath
    }
  }
  try{
    const {connector} = await AppConnector.init()

    if(to.meta.requiresAuth){
      try{
        await connector.isUserConnected()
        ConnectionStore.getUserIdentity()
      }
      catch (e) {
        return loginPage
      }
    }
    else if(to.name === 'LoginPage') {
      try{
        await connector.isUserConnected()
        ConnectionStore.getUserIdentity()
        return {name: 'StoragePage'}
      }
      catch (e) {}
    }
    return true
  }
  catch (e) {
    return loginPage
  }
})

export default router
