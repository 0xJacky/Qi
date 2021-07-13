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
                <a-select-option value="2021-2022-1">2021-2022-1</a-select-option>
                <a-select-option value="2020-2021-3">2020-2021-3</a-select-option>
                <a-select-option value="2020-2021-2">2020-2021-2</a-select-option>
                <a-select-option value="2020-2021-1">2020-2021-1</a-select-option>
            </a-select>
        </a-form-item>
        <a-button @click="get_exam_ics" type="primary">获取考试安排</a-button>
    </a-form>
</template>

<script>
import moment from "moment"

export default {
    name: "Exam",
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
        get_exam_ics() {
            let data = {}
            for (let k in this.formState) {
                data[k] = this.formState[k]
            }
            this.$api.check_user(data).then(r => {
                if (r.status) {
                    this.$message.success("登陆成功")
                    this.$message.info("正在解析")
                    this.$api.get_exam_ics(data).then(r => {
                        this.$message.success("解析成功")
                        const blob = new Blob(
                            [r.data], { type: 'text/calendar;charset=utf-8' })
                        const aEle = document.createElement('a');     // 创建a标签
                        const href = window.URL.createObjectURL(blob);       // 创建下载的链接
                        aEle.href = href;
                        aEle.download = this.formState.xnxqid + '-exam.ics'
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
