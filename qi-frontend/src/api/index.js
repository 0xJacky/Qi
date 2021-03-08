import http from "../lib/http"

const api = {
    check_user(data) {
        return http.post('/check_user', data)
    },

    get_course_ics(data) {
        return http.post('/course', data)
    }

}

export default api
