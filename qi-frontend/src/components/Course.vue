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
        <a-form-item label="学期开始">
            <a-date-picker
                v-model:value="formState.start_date"
                type="date"
            />
        </a-form-item>
        <a-button @click="get_course_ics" type="primary">获取课表</a-button>
    </a-form>
</template>

<script>
import moment from 'moment'
import 'moment/locale/zh-cn'

moment.locale('zh-cn')
export default {
    name: "Course",
    data() {
        return {
            cookies: this.$store.getters.cookies,
            semesters: ['2021-2022-1'],
            formState: {
                xnxqid: '2021-2022-1',
                start_date: moment('2021-09-01', 'YYYY-MM-DD')
            },
        }
    },
    created() {
        if (this.$route.query) {
            this.formState.xnxqid = this.$route.query.xnxqid
            this.formState.start_date = moment(this.$route.query.start_date??'2021-09-01', 'YYYY-MM-DD')
        }
        this.get_semesters()
    },
    watch: {
        formState: {
            handler() {
                this.$router.push({
                    query: {...this.formState, start_date: moment(this.formState.start_date).format('YYYY-MM-DD')}
                })
            },
            deep: true
        }
    },
    methods: {
        async get_semesters() {
            await this.check_user(this.cookies)
            this.$api.get_semesters(this.cookies).then(r => {
                this.formState.xnxqid = r.current
                this.semesters = r.semesters
            })
        },
        async check_user() {
            await this.$api.check_user().then(async r => {
                if (!r['success']) {
                    this.$message.info('Cookies 已过期，正在尝试重新登录', 10)
                    await this.$api.login(this.$store.getters.user).then(() => {
                        this.$message.success('登录成功')
                    }).catch(e => {
                        this.$message.error(e.error ? e.error : e)
                    })
                }
            })
        },
        async get_course_ics() {
            let data = {}
            for (let k in this.formState) {
                data[k] = this.formState[k]
            }
            data.start_date = data.start_date.format('YYYY-MM-DD')

            await this.check_user()

            this.$api.get_course_ics(data).then(r => {
                this.$message.success("解析成功")
                const blob = new Blob(
                    [r.data], {type: 'text/calendar;charset=utf-8'})
                const aEle = document.createElement('a');     // 创建a标签
                const href = window.URL.createObjectURL(blob);       // 创建下载的链接
                aEle.href = href;
                aEle.download = this.formState.xnxqid + '.ics'
                document.body.appendChild(aEle);
                aEle.click();
                document.body.removeChild(aEle)
                window.URL.revokeObjectURL(href)
            }).catch(r => {
                console.log(r)
                this.$message.error(r.error ? r.error : '解析失败，未知错误')
            })

        },
    }
}
</script>

<style scoped>

</style>
