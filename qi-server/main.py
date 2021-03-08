import tempfile

from flask import Flask, Response, request

from auth import Auth
from course import course_handler
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

app = Flask(__name__)


@app.route("/")
def homepage():
    return {
        "message": "Hello World"
    }


@app.route("/check_user", methods=['POST'])
def check_user():
    request_body = request.json
    auth = Auth()
    return {
        "status": auth.login(request_body['school_id'], request_body['password'])
    }


@app.route("/course", methods=['POST'])
def course():
    request_body = request.json

    with tempfile.TemporaryDirectory() as output_dir:
        file_path = \
            course_handler(request_body['school_id'],
                           request_body['password'],
                           request_body['xnxqid'],
                           request_body['start_date'],
                           output_dir)

        return {
            "data": open(file_path).read()
        }
