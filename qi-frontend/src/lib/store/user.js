export const user = {
    namespace: true,
    state: {
        school_id: null,
        password: null,
        cookies: null
    },
    mutations: {
        async login(state, payload) {
            state = Object.assign(state, payload)
        },
        logout(state) {
            sessionStorage.clear()
            state.school_id = null
            state.password = null
            state.cookies = null
        },
        update_user(state, payload) {
            state = Object.assign(state, payload)
        },
    },
    actions: {
        async login({commit}, data) {
            commit('login', data)
        },
        async logout({commit}) {
            commit('logout')
        },
        async update_user({commit}, data) {
            commit('update_user', data)
        },
    },
    getters: {
        user(state) {
            return {
                school_id: state.school_id,
                password: state.password
            }
        },
        cookies(state) {
            return state.cookies
        },
    }
}
