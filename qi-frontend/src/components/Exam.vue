<template>
    <a-form :model="formState">
        <a-form-item label="学年学期">
            <a-select
                v-model:value="formState.xnxqid"
                ref="select"
            >
                <a-select-option
                    v-for="s in semesters" :value="s" :key="s">
                    {{ s }}
                </a-select-option>
            </a-select>
        </a-form-item>
        <a-button @click="get_exam_ics" type="primary">获取考试安排</a-button>
    </a-form>
</template>

<script>
export default {
    name: "Exam",
    data() {
        return {
            semesters: [],
            formState: {
                xnxqid: '2021-2022-1',
            },
        }
    },
    created() {
        if (this.$route.query) {
            this.formState = Object.assign(this.formState, this.$route.query)
        }
        this.get_semesters()
    },
    watch: {
        formState: {
            handler() {
                this.$router.push({
                    query: this.formState
                })
            },
            deep: true
        }
    },
    methods: {
        async get_semesters() {
            await this.check_user()
            this.$api.get_semesters().then(r => {
                this.formState.xnxqid = r.current
                this.semesters = r.semesters
            })
        },
        async check_user() {
            await this.$api.check_user(this.cookies).then(async r => {
                if (!r['success']) {
                    await this.$api.login(this.$store.getters.user).then(() => {
                        this.$message.success('登录成功')
                    }).catch(e => {
                        this.$message.error(e.error ? e.error : e)
                    })
                }
            })
        },
        async get_exam_ics() {
            let data = {}
            for (let k in this.formState) {
                data[k] = this.formState[k]
            }
            await this.check_user()
            this.$message.info("正在解析")
            this.$api.get_exam_ics(data).then(r => {
                this.$message.success("解析成功")
                const blob = new Blob(
                    [r.data], {type: 'text/calendar;charset=utf-8'})
                const aEle = document.createElement('a');     // 创建a标签
                const href = window.URL.createObjectURL(blob);       // 创建下载的链接
                aEle.href = href;
                aEle.download = this.formState.xnxqid + '-exam.ics'
                document.body.appendChild(aEle);
                aEle.click();
                document.body.removeChild(aEle)
                window.URL.revokeObjectURL(href)
            }).catch(r => {
                this.$message.error(r.error ? r.error : '解析失败，未知错误')
            })
        }
    }
}
</script>

<style scoped>

</style>
