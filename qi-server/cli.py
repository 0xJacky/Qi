from config import config
from course import course_handler

school_id = config.get('user', 'name')
pwd = config.get('user', 'password')

xnxqid = config.get('core', 'xnxqid')
start_date = config.get('core', 'start_date')

course_handler(school_id, pwd, xnxqid, start_date)
