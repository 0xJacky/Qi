import datetime
import re

from bs4 import BeautifulSoup

from auth import Auth
from holiday import Holiday
from timetable import Timetable

timetable = Timetable()
holiday = Holiday()


def course_handler(school_id, pwd, xnxqid, start_date, output_dir='.'):
    auth = Auth(school_id, pwd)
    url = 'https://isea.sztu.edu.cn/jsxsd/xskb/xskb_list.do?xnxq01id=' + xnxqid
    start_date = start_date.split('-')
    r = auth.session.get(url, timeout=2)

    soup = BeautifulSoup(r.text, features='html.parser')

    tab = soup.findAll('table')[1]

    i = 0

    schedules = []

    for tr in tab.findAll('tr'):
        if '--------' in tr.getText():
            day = 0
            for td in tr.findAll('td'):
                # 过滤掉备注
                if '--------' in td.getText():
                    # print(td)
                    # 处理多节课占用同一时间段
                    td = str(td.find('div', class_='kbcontent')).replace('<br/>-----------<br/>',
                                                                         '</div><div class="kbcontent">')
                    # print(td)
                    td = BeautifulSoup(td, features='html.parser')
                    courses = td.find_all('div', class_='kbcontent')
                    # print(courses)
                    # print('星期%s' % str(day + 1))

                    for course in courses:
                        # 课程名称
                        course_name = course.contents[0]
                        # print(course_name)
                        # 周次
                        zc = course.find('font', title='周次(节次)').getText()
                        # fuck 1-18双周
                        ds = 0  # 不处理
                        if '单' in zc:
                            ds = 1
                        elif '双' in zc:
                            ds = 2
                        # 去除中文 周次里的 1-18(周) 单 双
                        zc = re.sub('[\u4e00-\u9fa5]', '', zc).replace('()', '')
                        _s = []
                        # 8,10,12,14,16 / 1-7,8-18
                        if ',' in zc:
                            zc = zc.split(',')
                            for s in zc:
                                if '-' in s:
                                    w_range = s.split('-')
                                    # print(w_range)
                                    _s += list(range(int(w_range[0]), int(w_range[1]) + 1))
                                else:
                                    _s.append(int(s))
                        else:
                            # 1-18
                            if '-' in zc:
                                # print(zc)
                                zc = zc.split('-')
                                # 1-18双周
                                zc_all = range(int(zc[0]), int(zc[1]) + 1)
                                s_tmp = []
                                if ds != 0:
                                    if ds == 2:
                                        for _zc in zc_all:
                                            if _zc % 2 == 0:
                                                s_tmp += [_zc]
                                    elif ds == 1:
                                        for _zc in zc_all:
                                            if _zc % 2:
                                                s_tmp += [_zc]
                                    _s = s_tmp
                                else:
                                    _s = list(zc_all)
                            # 2019-2020-1, 6
                            else:
                                _s += [int(zc)]

                        # print('周次: %s' % _s)
                        # 教室
                        classroom = course.find('font', title='教室').getText()
                        # print(classroom)
                        # 节次
                        section = re.findall(r'[\[](.+?)[]]', classroom)[0]
                        # 从 428机房[01-02-03-04]节 取出教室
                        classroom = classroom.split('[')[0]
                        if '-' in section:
                            section = section.split('-')

                            _tmp = []
                            for s in section:
                                _tmp += [int(s)]
                            section = _tmp

                        else:
                            section = [int(section)]

                        # print('节次:%s' % str(section))

                        # print('教室: %s' % classroom)
                        # print('==================')
                        tmp = {
                            'name': course_name,
                            'day': day,
                            'week': _s,
                            'section_index': section,
                            'location': classroom
                        }
                        schedules += [tmp]
                    # 统计节数
                    i += 1
                day += 1

    # 去重
    _schedules = []
    for item in schedules:
        if item not in _schedules:
            _schedules.append(item)
    schedules = _schedules

    print('课程总数:%s' % i)

    print(schedules)

    # 创建 ics
    ics = "%s/%s.ics" % (output_dir, xnxqid)
    message = ''
    f = open(ics, 'w', encoding='utf-8')
    f.write(u'BEGIN:VCALENDAR\nVERSION:2.0\n')
    for course in schedules:
        date = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        hour = timetable.translate(course['section_index'])

        for w in course['week']:
            day = (date + datetime.timedelta(days=course['day'] + 7 * (int(w) - 1)))

            # 处理假期及补课
            if holiday.is_holiday(day.strftime('%Y-%m-%d')):
                m = holiday.makeup(day.strftime('%Y-%m-%d'))
                if m:
                    day = m
                else:
                    continue

            day = day.strftime('%Y%m%d')

            message += '''BEGIN:VEVENT
SUMMARY:%s
DTSTART;TZID="UTC+08:00";VALUE=DATE-TIME:%sT%s
DTEND;TZID="UTC+08:00";VALUE=DATE-TIME:%sT%s
LOCATION:%s
END:VEVENT

''' % (course['name'], day, hour[0], day, hour[1], course['location'])

    print(message)
    f.write(message)

    f.write(u'END:VCALENDAR')
    f.close()

    return ics
