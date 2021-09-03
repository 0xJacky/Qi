import codecs
import json
import sys
import tempfile

import flask
from flask import Flask, request

from auth2 import Auth
from course_excel import course_excel_handler
from exam import exam_handler
from semester import get_semester
from transposition import get_college_and_grade_list, get_major_list, transposition

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

app = Flask(__name__)


@app.route("/")
def homepage():
    return {
        "message": "Hello World"
    }


@app.route("/login", methods=['POST'])
def login():
    request_body = request.json
    auth = Auth()
    cookies, ok = auth.login(request_body['school_id'], request_body['password'])
    if ok:
        return {
            "cookies": cookies
        }
    else:
        return {
                   "error": "登录失败，学号或密码错误",
               }, 403


@app.route("/check_user", methods=['POST'])
def check_user():
    cookies = request.headers.get('Q-COOKIES')
    cookies = json.loads(cookies)
    auth = Auth(cookies)
    auth.check_login()
    return {
        "success": auth.ok
    }


@app.route("/semesters", methods=['GET'])
def semesters():
    try:
        cookies = request.headers.get('Q-COOKIES')
        cookies = json.loads(cookies)
        semester, selected = get_semester(cookies)
        return {
            "semesters": semester,
            "current": selected
        }

    except Exception as e:
        return {
                   "error": str(e)
               }, 500


@app.route("/course", methods=['POST'])
def course():
    request_body = request.json

    cookies = request.headers.get('Q-COOKIES')
    cookies = json.loads(cookies)

    with tempfile.TemporaryDirectory() as output_dir:
        try:
            file_path = \
                course_excel_handler(cookies,
                                     request_body['xnxqid'],
                                     request_body['start_date'],
                                     output_dir)

            return {
                "data": open(file_path).read()
            }
        except Exception as e:
            return {
                       "error": str(e)
                   }, 500


@app.route("/exam", methods=['POST'])
def exam():
    request_body = request.json

    with tempfile.TemporaryDirectory() as output_dir:
        try:
            cookies = request.headers.get('Q-COOKIES')
            cookies = json.loads(cookies)
            file_path = \
                exam_handler(cookies,
                             request_body['xnxqid'],
                             output_dir)

            return {
                "data": open(file_path).read()
            }
        except Exception as e:
            return {
                       "error": str(e)
                   }, 500


@app.route("/colleges_and_grades", methods=['GET'])
def college_and_grade():
    try:
        cookies = request.headers.get('Q-COOKIES')
        cookies = json.loads(cookies)

        c, g = get_college_and_grade_list(cookies)
        return {
            "colleges": c,
            "grades": g
        }
    except Exception as e:
        return {
                   "error": str(e)
               }, 500


@app.route("/majors", methods=['GET'])
def majors():
    try:
        cookies = request.headers.get('Q-COOKIES')
        cookies = json.loads(cookies)
        _majors = get_major_list(cookies, request.args.get('college_id'), request.args.get('grade'))
        return {
            "majors": _majors
        }
    except Exception as e:
        return {
                   "error": str(e)
               }, 500


@app.route("/transposition", methods=['POST'])
def get_transposition():
    request_body = request.json
    try:
        with tempfile.TemporaryDirectory() as output_dir:
            cookies = request.headers.get('Q-COOKIES')
            cookies = json.loads(cookies)
            file_path = transposition(cookies, output_dir, request_body['xnxqid'], request_body['college_id'],
                                      request_body['grade'], request_body['major_id'])
            return flask.send_file(file_path, as_attachment=True)
    except Exception as e:
        return {
                   "error": str(e)
               }, 500
