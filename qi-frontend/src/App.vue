<template>
    <a-config-provider :locale="locale">
        <div class="project-title">
            <h1>Project Qi</h1>
            <h2>教务系统工具</h2>
        </div>
        <a-tabs v-model:activeKey="activeKey">
            <a-tab-pane key="0" tab="课程表">
                <course/>
            </a-tab-pane>
            <!--<a-tab-pane key="1" tab="Tab 2" disabled>

            </a-tab-pane>-->
            <a-tab-pane key="3" tab="关于">
                <about/>
            </a-tab-pane>
        </a-tabs>
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

export default {
    name: 'App',
    components: {Course, About},
    data() {
        return {
            locale: zhCN,
            activeKey: ref('0'),
            thisYear: new Date().getFullYear()
        }
    },
}
</script>

<style lang="less">
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
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

footer {
    padding: 30px;
}
</style>
