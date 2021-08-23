<template>
    <a-config-provider :locale="locale">
        <div class="project-title">
            <h1>Project Qi</h1>
            <h2>教务系统工具</h2>
        </div>
        <login/>
        <transition name="fade">
            <a-tabs v-model:activeKey="activeKey"  v-if="user.school_id">
                <a-tab-pane key="0" tab="课程表">
                    <course/>
                </a-tab-pane>
                <a-tab-pane key="1" tab="考试安排">
                    <exam/>
                </a-tab-pane>
                <a-tab-pane key="2" tab="课表转置" disabled>
                    <Transposition/>
                </a-tab-pane>
                <a-tab-pane key="3" tab="关于">
                    <about/>
                </a-tab-pane>
            </a-tabs>
        </transition>
        <footer>
            Copyright © 2020 - {{ thisYear }} 余圳曦
        </footer>
    </a-config-provider>
</template>


<script>
import {ref} from 'vue'
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import Course from "./components/Course"
import About from "./components/About"
import Exam from "./components/Exam"
import Transposition from "./components/Transposition"
import Login from "@/components/Login"

export default {
    name: 'App',
    components: {Login, Transposition, Exam, Course, About},
    data() {
        return {
            locale: zhCN,
            activeKey: ref('0'),
            thisYear: new Date().getFullYear()
        }
    },
    computed: {
        user() {
            return this.$store.getters.user
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

#app {
    font-family: "PingFang SC", Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin: 0 auto;
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

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

footer {
    padding: 30px;
}
</style>
