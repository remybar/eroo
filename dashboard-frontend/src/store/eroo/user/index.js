const axios = require('axios')

const SET_USERNAME = 'SET_USERNAME'

export default {
  namespaced: true,
  state: {
    userName: null,
  },
  getters: {
    userName(state) {
      return state.userName
    },
  },
  mutations: {
    [SET_USERNAME](state, userName) {
      console.log('mutate username', userName)
      state.userName = userName
    },
  },
  actions: {
    getCurrentUserName({ commit }) {
      axios.get('/api/v1/user/username')
        .then(response => {
          console.log(`userName: ${response.userName}`)
          commit(SET_USERNAME, response.userName)
        })
        .catch(error => {
          console.log(error)
        })
    },
  },
}
