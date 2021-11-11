import appConfigStoreModule from '@core/@app-config/appConfigStoreModule'
import Vue from 'vue'
import Vuex from 'vuex'
import app from './app'
import housings from './eroo/housing'
import seasons from './eroo/seasons'

Vue.use(Vuex)
Vue.config.devtools = true

export default new Vuex.Store({
  state: {
    config: JSON.parse(document.getElementById('config').textContent),
  },
  getters: {
    urls: state => state.config.urls,
  },
  mutations: {},
  actions: {},
  modules: {
    appConfig: appConfigStoreModule,
    app,
    housings,
    seasons,
  },
})
