import argparse
from config import config
from course import course_handler
from exam import exam_handler
from auth2 import Auth

parser = argparse.ArgumentParser(description='Project Qi CLi')
parser.add_argument('-c', '--course', action="store_true", help='get course ics')
parser.add_argument('-e', '--exam', action="store_true", help='get exam ics')
args = parser.parse_args()

school_id = config.get('user', 'name')
pwd = config.get('user', 'password')

xnxqid = config.get('core', 'xnxqid')
start_date = config.get('core', 'start_date')
auth = Auth()
cookies, ok = auth.login(school_id, pwd)
if not ok:
    print('login fail')
    exit()

if args.course:
    course_handler(cookies, xnxqid, start_date)
elif args.exam:
    exam_handler(cookies, xnxqid)
else:
    print('args error')
