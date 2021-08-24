import http from "@/lib/http"
import app from '@/main'
import {store} from "@/lib/store"

const api = {
    async login(data) {
        await store.dispatch('login_lock')
        return http.post('/login', data).then(async r => {
            await app.config.globalProperties.$store.commit('login', {
                ...data,
                ...r
            })
        }).finally(async () => {
            await store.dispatch('login_unlock')
        })
    },

    check_user() {
        return http.post('/check_user')
    },

    get_semesters() {
        return http.get('/semesters')
    },

    get_college_and_grade() {
        return http.get('/colleges_and_grades')
    },

    get_majors(college_id, grade) {
        return http.get('/majors', {
            params: {
                college_id: college_id,
                grade: grade
            }
        })
    },

    get_transposition(data) {
        return http.post('/transposition', data, {
            responseType: 'arraybuffer'
        })
    },

    get_course_ics(data) {
        return http.post('/course', data)
    },

    get_exam_ics(data) {
        return http.post('/exam', data)
    }

}

export default api
