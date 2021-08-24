<template>
    <div class="loading" v-if="loading">
        <div class="wrapper">
            <div class="center-content">
                <a-spin :indicator="indicator"/>
                <div class="text">
                    <p>{{ text }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {LoadingOutlined} from '@ant-design/icons-vue'
import {defineComponent, h} from 'vue'

export default defineComponent({
    setup() {
        const indicator = h(LoadingOutlined, {
            style: {
                fontSize: '24px',
            },
            spin: true,
        })
        return {
            indicator,
        }
    },
    props: ['loading', 'text']
})
</script>

<style lang="less">
.loading {
    position: fixed;
    background: #ffffff;
    @media (prefers-color-scheme: dark) {
        background: #1e1f20;
    }
    z-index: 10;
    width: 100%;
    height: 100%;
    top: 0;
    right: 0;

    .wrapper {
        position: relative;
        display: inline-grid;
        align-items: center;
        height: 100%;

        .ant-spin {
            position: unset;
        }
        .center-content {
            .text {
                padding: 10px;
            }
        }
    }
}
</style>
