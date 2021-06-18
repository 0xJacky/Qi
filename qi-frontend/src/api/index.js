import http from "../lib/http"

const api = {
    check_user(data) {
        return http.post('/check_user', data)
    },

    get_course_ics(data) {
        return http.post('/course', data)
    },

    get_exam_ics(data) {
        return http.post('/exam', data)
    }

}

export default api
