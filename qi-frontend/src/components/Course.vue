<template>
    <a-form :model="formState">
        <a-form-item label="学号">
            <a-input v-model:value="formState.school_id"/>
        </a-form-item>
        <a-form-item label="密码">
            <a-input type="password" v-model:value="formState.password"/>
        </a-form-item>
        <a-form-item label="学年学期">
            <a-select
                v-model:value="formState.xnxqid"
                ref="select"
            >
                <a-select-option value="2020-2021-2">2020-2021-2</a-select-option>
                <a-select-option value="2020-2021-1">2020-2021-1</a-select-option>
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
import moment from "moment"

export default {
    name: "Course",
    data() {
        return {
            formState: {
                school_id: '',
                password: '',
                xnxqid: '2020-2021-2',
                start_date: moment('2021-03-01', 'YYYY-MM-DD')
            },
        }
    },
    methods: {
        get_course_ics() {
            let data = {}
            for (let k in this.formState) {
                data[k] = this.formState[k]
            }
            data.start_date = data.start_date.format('YYYY-MM-DD')
            this.$api.check_user(data).then(r => {
                if (r.status) {
                    this.$message.success("登陆成功")
                    this.$message.info("正在解析")
                    this.$api.get_course_ics(data).then(r => {
                        this.$message.success("解析成功")
                        const blob = new Blob(
                            [r.data], { type: 'text/calendar;charset=utf-8' })
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
                        this.$message.error("解析失败")
                    })
                } else {
                    this.$message.error("无法登陆 账号或密码错误")
                }
            })
        }
    }
}
</script>

<style scoped>

</style>
