import { createStore } from 'vuex'
import {user} from './user'
import VuexPersistence from 'vuex-persist'


const debug = process.env.NODE_ENV !== 'production'

const vuexLocal = new VuexPersistence({
    storage: window.localStorage,
    modules: ['user']
})

export const store = createStore({
    // 将各组件分别模块化存入 Store
    modules: {
        user
    },
    plugins: [vuexLocal.plugin],
    strict: debug
})
