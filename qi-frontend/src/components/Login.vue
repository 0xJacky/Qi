<template>
    <div>
        <transition name="fade">
            <a-form layout="vertical" class="login-form" :model="formState" v-if="!user.school_id">
                <a-form-item label="学号">
                    <a-input v-model:value="formState.school_id"/>
                </a-form-item>
                <a-form-item label="密码">
                    <a-input type="password" v-model:value="formState.password"/>
                </a-form-item>
                <a-button type="primary" @click="login">登陆</a-button>
            </a-form>
            <div v-else>
                <p>当前用户: {{ user.school_id }}</p>
                <a-button @click="logout">更换用户</a-button>
            </div>
        </transition>
    </div>
</template>

<script>
export default {
    name: "Login",
    data() {
        return {
            formState: {
                school_id: '',
                password: ''
            }
        }
    },
    methods: {
        async login() {
            if (!(this.formState.school_id && this.formState.password)) {
                this.$message.error("请输入用户名与密码")
                return
            }
            this.$message.info("受新版教务系统统一认证的影响，此过程将会持续1-10秒", 10)
            this.$api.login(this.formState).then(() => {
                this.$message.success('登录成功')
            }).catch(e => {
                this.$message.error(e.error ? e.error : e)
            })
        },
        async logout() {
            this.$store.commit('logout')
        }
    },
    computed: {
        user() {
            return this.$store.getters.user
        }
    }
}
</script>

<style lang="less" scoped>
.login-form {
    margin: 0 auto;
    max-width: 300px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
