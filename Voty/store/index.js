export const state = () => ({
    user: null
  });
  
  export const mutations = {
    SET_USER(state, user) {
      state.user = user;
    },
    REMOVE_USER(state) {
      state.user = null;
    }
  };
  export const getters = {
    getUser(state) {
      return state.user;
    }
  };