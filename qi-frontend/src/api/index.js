import http from "@/lib/http"
import app from '@/main'

const api = {
    login(data) {
        return http.post('/login', data).then(async r => {
            await app.config.globalProperties.$store.commit('login', {
                ...data,
                ...r
            })
        })
    },
    check_user(data) {
        return http.post('/check_user', data)
    },

    get_course_ics(data) {
        return http.post('/course', {
            cookies: app.config.globalProperties.$store.getters.cookies,
            ...data
        })
    },

    get_exam_ics(data) {
        return http.post('/exam', {
            cookies: app.config.globalProperties.$store.getters.cookies,
            ...data
        })
    }

}

export default api
