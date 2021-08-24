export const user = {
    namespace: true,
    state: {
        school_id: null,
        password: null,
        cookies: null,
        login_lock: false,
    },
    mutations: {
        async lock(state, status) {
            state.login_lock = status
        },
        async login(state, payload) {
            state = Object.assign(state, payload)
        },
        logout(state) {
            sessionStorage.clear()
            state.school_id = null
            state.password = null
            state.cookies = null
            state.login_lock = false
        },
        update_user(state, payload) {
            state = Object.assign(state, payload)
        },
    },
    actions: {
        async login_lock({commit}) {
            commit('lock', true)
        },
        async login_unlock({commit}) {
            commit('lock', false)
        },
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
        login_lock(state) {
            return state.login_lock
        },
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
