export const routes = [{
    path: "/",
    name: "课表解析",
    component: () => import('@/components/Course')
}, {
    path: "/exam",
    name: "考试安排解析",
    component: () => import('@/components/Exam')
}, {
    path: "/transposition",
    name: "班级理论课表转置",
    component: () => import('@/components/Transposition')
}, {
    path: "/about",
    name: "关于",
    component: () => import('@/components/About')
}]
