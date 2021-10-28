import appConfigStoreModule from '@core/@app-config/appConfigStoreModule'
import Vue from 'vue'
import Vuex from 'vuex'
import app from './app'
import erooHousing from './eroo/housing'
import erooUser from './eroo/user'

Vue.use(Vuex)
Vue.config.devtools = true

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    appConfig: appConfigStoreModule,
    app,
    erooHousing,
    erooUser,
  },
})
