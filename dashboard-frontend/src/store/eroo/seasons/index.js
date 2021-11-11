import http from '@/http'

export const INIT_SEASONS = 'INIT_SEASONS'
export const SET_SEASON = 'SET_SEASON'
export const DELETE_SEASON = 'DELETE_SEASON'

export default {
  namespaced: true,
  state: {
    seasons: {},
  },
  getters: {
    getSeasonsByHousing: state => housingId => state.seasons.filter(s => s.housingId === housingId),
  },
  mutations: {
    [INIT_SEASONS](state, seasons) {
      state.seasons = seasons
    },
    [SET_SEASON](state, { seasonId, season }) {
      state.seasons[seasonId] = season
    },
    [DELETE_SEASON](state, seasonId) {
      delete state.seasons[seasonId]
    },
  },
  actions: {
    list({ commit, rootState }) {
      http.get(rootState.config.urls.seasons.list)
        .then(res => res.json())
        .then(
          payload => commit(INIT_SEASONS, payload),
          error => console.log(`erreur: ${error}`),
        )
    },
    create({ commit, rootState }, season) {
      http.post(rootState.config.urls.seasons.create, season)
        .then(res => res.json())
        .then(
          id => commit(SET_SEASON, { id, season }),
          error => console.log(`erreur: ${error}`),
        )
    },
    update({ commit, rootState }, id, season) {
      http.post(`${rootState.config.urls.seasons.update}/{id}`, season)
        .then(
          () => commit(SET_SEASON, { id, season }),
          error => console.log(`erreur: ${error}`),
        )
    },
    delete({ commit, rootState }, id) {
      http.post(`${rootState.config.urls.seasons.delete}/{id}`)
        .then(
          () => commit(DELETE_SEASON, { id }),
          error => console.log(`erreur: ${error}`),
        )
    },
  },
}
