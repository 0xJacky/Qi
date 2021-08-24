<template>
    <div>
        <p>实在是想不明白为什么会从周一到周五横着展示课表，
            所以有了这个转置工具，将会导出 Excel，按班级分页，横向是星期，纵方向是节次，方便选课。</p>
        <a-form :model="formState" :labelCol="{span:5}" :wrapperCol="{span:15}">
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

            <a-form-item label="学院">
                <a-select
                    v-model:value="formState.college_id"
                    ref="select"
                >
                    <a-select-option
                        v-for="(v,k) in colleges" :value="k" :key="k">
                        {{ v }}
                    </a-select-option>
                </a-select>
            </a-form-item>

            <a-form-item label="上课年级">
                <a-select
                    v-model:value="formState.grade"
                    ref="select"
                >
                    <a-select-option
                        v-for="s in grades" :value="s" :key="s">
                        {{ s }}
                    </a-select-option>
                </a-select>
            </a-form-item>

            <a-form-item label="专业">
                <a-select
                    v-model:value="formState.major_id"
                    ref="select"
                >
                    <a-select-option
                        v-for="(v,k) in majors" :value="k" :key="k">
                        {{ v }}
                    </a-select-option>
                </a-select>
            </a-form-item>
        </a-form>
        <a-button type="primary" @click="get">下载 Excel</a-button>
    </div>
</template>

<script>
export default {
    name: "Transposition",
    data() {
        return {
            formState: {
                xnxqid: '',
                college_id: '',
                grade: '',
                major_id: ''
            },
            semesters: [],
            colleges: [],
            grades: [],
            majors: []
        }
    },
    async created() {
        if (this.$route.query) {
            this.formState = Object.assign(this.formState, this.$route.query)
        }
        await this.check_user()
        this.$api.get_semesters().then(r => {
            this.semesters = r.semesters
        })
        this.$api.get_college_and_grade().then(r => {
            this.colleges = r.colleges
            this.grades = r.grades
        })
    },
    watch: {
        formState: {
            handler() {
                const {college_id, grade} = this.formState
                this.$router.push({
                    query: this.formState
                })
                if (college_id && grade) {
                    this.$api.get_majors(college_id, grade).then(r => {
                        this.majors = r.majors
                    })
                }
            },
            deep: true
        }
    },
    methods: {
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
        get() {
            this.$api.get_transposition(this.formState).then(r => {
                this.$message.success("解析成功")
                const blob = new Blob(
                    [r],
                    {
                        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;'
                    })
                const aEle = document.createElement('a');     // 创建a标签
                const href = window.URL.createObjectURL(blob);       // 创建下载的链接
                aEle.href = href;
                const filename = `${this.formState.xnxqid}-${this.colleges[this.formState.college_id]}-${this.formState.grade}-${this.majors[this.formState.major_id]}`
                aEle.download = `${filename}.xlsx`
                document.body.appendChild(aEle)
                aEle.click();
                document.body.removeChild(aEle)
                window.URL.revokeObjectURL(href)

            }).catch(r => {
                console.log(r)
                this.$message.error(r.error ? r.error : '解析失败，未知错误')
            })
        }
    }

}
</script>

<style lang="less" scoped>

</style>
