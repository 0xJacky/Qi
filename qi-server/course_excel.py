import datetime
import os
import re
import tempfile

import xlrd

from auth2 import Auth
from holiday import Holiday
from timetable import Timetable

timetable = Timetable()
holiday = Holiday()


def handle_zc(zc):
    # 周次
    # fuck 1-18双周
    ds = 0  # 不处理
    if '单' in zc:
        ds = 1
    elif '双' in zc:
        ds = 2

    # 节次
    zc = zc.replace('节', '')
    zc = zc.replace('([周])', '(周)')
    section = re.findall(r'[\[](.+?)[]]', zc)[0]

    zc = zc.split('[')[0]
    # 去除中文 周次里的 1-18(周) 单 双
    zc = re.sub('[\u4e00-\u9fa5]', '', zc).replace('()', '')
    _s = []
    # 8,10,12,14,16 / 1-7,8-18
    print(zc)
    if ',' in zc:
        zc = zc.split(',')
        for s in zc:
            if '-' in s:
                w_range = s.split('-')
                print(w_range)
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

    # 节次
    if '-' in section:
        section = section.split('-')

        _tmp = []
        for s in section:
            _tmp += [int(s)]
        section = _tmp

    else:
        section = [int(section)]

    return _s, section


def course_excel_handler(cookies, xnxqid, start_date, output_dir='.'):
    auth = Auth(cookies)

    if not auth.ok:
        raise Exception('登录失败，请检查用户名密码')

    url = 'https://jwxt.sztu.edu.cn/jsxsd/xskb/xskb_print.do?' \
          'xnxq01id=%s&zc=&kbjcmsid=EB5693B95B204102B2E28C5624C6E9ED&wkbkc=1' % xnxqid

    start_date = start_date.split('-')
    r = auth.get_excel(url)
    schedules = []
    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, 'course_excel.xls')
        excel_file = open(path, 'wb')
        excel_file.write(r.content)
        excel_file.close()
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        for i in range(3, 9):
            for j in range(1, 8):
                value = sheet.cell(i, j).value
                value = value.strip()
                # 多节课占用同一时间段
                value = value.split('\n\n')
                for k in range(len(value)):
                    value[k] = value[k].split('\n')
                    if value[k][0] == '':
                        continue
                    zc, section = handle_zc(value[k][3])
                    tmp = {
                        'name': value[k][0],
                        'week': zc,
                        'section_index': section,
                        'location': value[k][4],
                        'day': j - 1,
                    }
                    schedules.append(tmp)
                print('第%s节,周%s %s' % (i - 2, j, value))
            print()

    print(schedules)

    # 创建 ics
    ics = "%s/%s.ics" % (output_dir, xnxqid)
    message = ''
    f = open(ics, 'w', encoding='utf-8')
    f.write(u'BEGIN:VCALENDAR\nVERSION:2.0\n')
    for course in schedules:
        start = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        date = start - datetime.timedelta(start.weekday())
        hour = timetable.translate(course['section_index'])

        for w in course['week']:
            day = (date + datetime.timedelta(days=course['day'] + 7 * (int(w) - 1)))
            if day < start:
                continue
            # 处理假期及补课
            if holiday.is_holiday(day.strftime('%Y-%m-%d')):
                m = holiday.makeup(day.strftime('%Y-%m-%d'))
                if m:
                    day = m
                else:
                    continue

            day = day.strftime('%Y%m%d')

            message += '''
BEGIN:VEVENT
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


# cookies = {"JSESSIONID": "FB36FC3571402865C5E4EFC2846B6831", "SERVERID": "122"}
# course_excel_handler(cookies, '2021-2022-1', '2021-09-02', '.')
