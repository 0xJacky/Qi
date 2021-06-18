<template>
    <div>
        <p>将教务系统内的课程表、考试安排解析为 ics 日历文件，您可以将 ics 日历文件导入 iOS、安卓系统的日历中</p>
        <p>Q: Apple 设备如何导入 ics 文件？</p>
        <p>A: 请参考 <a href="https://jackyu.cn/tech/apple-ics-import/" target="_blank">https://jackyu.cn/tech/apple-ics-import/</a></p>
        <p>Q: 项目介绍及 iOS 捷径</p>
        <p>A: 请参考 <a href="https://jackyu.cn/projects/qi/">https://jackyu.cn/projects/qi/</a></p>
        <h3>技术栈</h3>
        <p>前端 Vue3 后端 Flask 环境 Docker</p>
        <h3>项目组</h3>
        <p>全栈: 0xJacky</p>
        <p>项目地址：<a href="https://github.com/0xJacky/Qi">https://github.com/0xJacky/Qi</a></p>
        <p>公共测试阶段，bug 请联系 me@jackyu.cn</p>
        <h3>产品说明</h3>
        <p>1. Qi 支持手动维护的放假、补课安排，配置信息在 holiday.py，欢迎通过提交 PR 补充假期安排</p>
        <p>2. <strong>学号及密码仅用于请求教务系统</strong></p>
        <p>3. ics 文件导入 iOS 日历，请将 ics 通过邮件发送到 iOS 设备上，通过系统自带的邮件 App 可以直接将日历导入，建议在导入前新建一个新的日历分区</p>
        <p>4. macOS 用户可以直接导入 ics 文件</p>
        <h3>补课安排</h3>
        <p>1. 2020年国庆及中秋节放假、补课安排</p>
        <p>2. 2021年元旦、清明、五一、端午放假安排</p>
    </div>
</template>

<script>
export default {
    name: "About"
}
</script>

<style scoped>

</style>
