import {createApp} from 'vue'
import App from './App.vue'
import http from "./lib/http"

import {
    Button,
    message,
    DatePicker,
    Form,
    Input,
    ConfigProvider,
    Tabs,
    Select
} from 'ant-design-vue'

import api from "./api"

import VueGtag from "vue-gtag-next"

const app = createApp(App)

app.use(Button)
app.config.globalProperties.$message = message
app.use(DatePicker)
app.use(Form)
app.use(Input)
app.use(ConfigProvider)
app.use(Tabs)
app.use(Select)

app.config.globalProperties.$http = http
app.config.globalProperties.$api = api

app.use(VueGtag, {
    property: {
        id: "G-TM8GG5FXMR"
    },
    isEnabled: process.env.NODE_ENV === 'production'
})

app.mount('#app')
