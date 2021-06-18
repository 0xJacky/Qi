import argparse
from config import config
from course import course_handler
from exam import exam_handler

parser = argparse.ArgumentParser(description='Project Qi CLi')
parser.add_argument('-c', '--course', action="store_true", help='get course ics')
parser.add_argument('-e', '--exam', action="store_true", help='get exam ics')
args = parser.parse_args()

school_id = config.get('user', 'name')
pwd = config.get('user', 'password')

xnxqid = config.get('core', 'xnxqid')
start_date = config.get('core', 'start_date')

if args.course:
    course_handler(school_id, pwd, xnxqid, start_date)
elif args.exam:
    exam_handler(school_id, pwd, xnxqid)
else:
    print('args error')
