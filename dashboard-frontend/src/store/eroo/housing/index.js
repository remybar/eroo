import Vue from 'vue'
import http from '@/http'

export const INIT_HOUSING = 'INIT_HOUSING'
export const SET_HOUSING = 'SET_HOUSING'
export const DELETE_HOUSING = 'DELETE_HOUSING'

export default {
  namespaced: true,
  state: {
    housings: {},
  },
  getters: {
    hasHousings: state => state.housings.length > 0,
  },
  mutations: {
    [INIT_HOUSING](state, housings) {
      state.housings = housings
    },
    [SET_HOUSING](state, { id, housing }) {
      Vue.set(state.housings, id, housing)
    },
    [DELETE_HOUSING](state, { id }) {
      delete state.housings[id]
    },
  },
  actions: {
    list({ commit, rootState }) {
      http.get(rootState.config.urls.housings.list)
        .then(
          res => commit(INIT_HOUSING, res.data),
          error => console.log(`TODO BAR erreur: ${error}`),
        )
    },
    async create({ commit, rootState }, housing) {
      return http.post(rootState.config.urls.housings.create, housing)
        .then(
          res => {
            const { id } = res.data
            commit(SET_HOUSING, { id, housing })

            return id
          },
          error => error,
        )
    },
    update({ commit, rootState }, id, housing) {
      http.post(`${rootState.config.urls.housings.update}/{id}`, housing)
        .then(
          () => commit(SET_HOUSING, { id, housing }),
          error => console.log(`TODO BAR erreur: ${error}`),
        )
    },
    delete({ commit, rootState }, id) {
      http.post(`${rootState.config.urls.housings.delete}/{id}`)
        .then(
          () => commit(DELETE_HOUSING, { id }),
          error => console.log(`TODO BAR erreur: ${error}`),
        )
    },
  },
}
