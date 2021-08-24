import {createApp} from 'vue'
import App from './App.vue'
import http from "./lib/http"
import {createRouter, createWebHistory} from "vue-router";

import {
    Button,
    message,
    DatePicker,
    Form,
    Input,
    ConfigProvider,
    Menu,
    Select,
    Spin,
    Icon
} from 'ant-design-vue'

import 'ant-design-vue/dist/antd.less'

import api from "./api"
import {store} from './lib/store'

import VueGtag from "vue-gtag-next"

const app = createApp(App)
app.use(Button)
app.config.globalProperties.$message = message
app.use(DatePicker)
app.use(Form)
app.use(Input)
app.use(ConfigProvider)
app.use(Menu)
app.use(Select)
app.use(Spin)
app.use(Icon)
app.use(store)

app.config.globalProperties.$http = http
app.config.globalProperties.$api = api

app.use(VueGtag, {
    property: {
        id: "G-TM8GG5FXMR"
    },
    isEnabled: process.env.NODE_ENV === 'production'
})

import {routes} from "@/routes"
const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

app.use(router)

app.mount('#app')


export default app
