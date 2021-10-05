<template>
    <a-config-provider :locale="locale">
        <div class="project-title">
            <h1>Project Qi</h1>
            <h2>教务系统工具</h2>
        </div>
        <login/>
        <div v-show="user.school_id&&!login_lock">
            <a-menu v-model:selectedKeys="current" mode="horizontal">
                <a-menu-item v-for="r in routes" :key="r.path">
                    <router-link :to="r.path">
                        {{ r.name }}
                    </router-link>
                </a-menu-item>
            </a-menu>
            <div class="container">
                <router-view v-slot="{ Component }">
                    <transition name="fade">
                        <component :is="Component"/>
                    </transition>
                </router-view>
            </div>
        </div>
        <loading :loading="login_lock" text="请稍等，新版教务系统认证需要 3-10s"/>
        <footer>
            Copyright © 2020 - {{ thisYear }} 余圳曦<br/>
            版本 {{ version }} ({{ build }})
        </footer>
    </a-config-provider>
</template>


<script>
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import Login from "@/components/Login"
import {routes} from "@/routes"
import Loading from "@/components/Loading"

export default {
    name: 'App',
    components: {Loading, Login},
    data() {
        return {
            locale: zhCN,
            routes,
            version: process.env.VUE_APP_VERSION,
            build: process.env.VUE_APP_BUILD_ID ?? '开发模式',
            current: [this.$route.path],
            thisYear: new Date().getFullYear()
        }
    },
    created() {
        this.$store.dispatch('login_unlock')
    },
    watch: {
        '$route'() {
            this.current = [this.$route.path]
        }
    },
    computed: {
        user() {
            return this.$store.getters.user
        },
        login_lock() {
            return this.$store.getters.login_lock
        }
    }
}
</script>

<style lang="less">
@media (prefers-color-scheme: dark) {
    @import '~ant-design-vue/dist/antd.dark.less';
    @border-radius-base: 2px;
}

@media (prefers-color-scheme: light) {
    @border-radius-base: 2px;
}

body {
    position: relative;
}

#app {
    font-family: "PingFang SC", Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin: 0 auto;
    width: 80%;
    max-width: 500px;
}

.ant-tabs {
    margin: 30px;
}

.project-title {
    margin: 50px;

    h1 {
        font-weight: 300;
    }

    h2 {
        font-weight: 200;
    }
}

.container {
    padding: 20px 5px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

footer {
    padding: 30px;
}
</style>
