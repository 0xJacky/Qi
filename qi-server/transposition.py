import json
import os

import xlsxwriter
from bs4 import BeautifulSoup

from auth2 import Auth


def get_college_and_grade_list(cookies):
    auth = Auth(cookies)
    r = auth.get('https://jwxt.sztu.edu.cn/jsxsd/kbcx/kbxx_xzb')
    soup = BeautifulSoup(r.text, features='html.parser')

    options = soup.find('select', id='skyx')
    options = options.findAll('option')
    college_list = {}

    for option in options:
        college_list[option['value']] = option.getText()

    options = soup.find('select', id='sknj')
    options = options.findAll('option')
    grade_list = []
    for option in options:
        grade_list.append(option.getText())

    return college_list, grade_list


def get_major_list(cookies, college_id, grade):
    auth = Auth(cookies)
    r = auth.get('https://jwxt.sztu.edu.cn/jsxsd/kbcx/getZyByAjax?&skyx=%s&sknj=%s'
                 % (college_id, grade))

    r = json.loads(r.text)
    res = {}
    for m in r:
        res[m['dm']] = m['dmmc']
    return res


def transposition(cookies, output, xnxq, college_id, grade, major_id):
    auth = Auth(cookies)

    data = {
        'xnxqh': xnxq,
        'kbjcmsid': 'EB5693B95B204102B2E28C5624C6E9ED',
        'skyx': college_id,
        'sknj': grade,
        'skzy': major_id
    }

    r = auth.post('https://jwxt.sztu.edu.cn/jsxsd/kbcx/kbxx_xzb_ifr', data)
    soup = BeautifulSoup(r.text, features='html.parser')

    tab = soup.findAll('table')[0]

    # print(len(tab.findAll('tr')))

    tr = tab.findAll('tr')

    # 定义 excel 操作句柄
    path = os.path.join(output, '课表.xlsx')
    o = xlsxwriter.Workbook(path)
    workfomat = o.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True,
    })

    for i in range(2, len(tr)):
        # print(tr[i])
        td = tr[i].findAll('td')
        cnt = 0

        _class = td[0].findAll('nobr')[0].text
        print(_class)

        e = o.add_worksheet(u'班级' + str(_class))

        week = tr[0].findAll('th')
        # 星期几
        for j in range(1, 8):
            print(week[j].text)
            e.write(0, j, week[j].text, workfomat)

        # 节次
        section = tr[1].findAll('td')
        for j in range(1, 7):
            print(section[j].text)
            e.write(j, 0, section[j].text, workfomat)

        # 具体课程
        for j in range(1, len(td)):
            course_info = td[j].findAll('div', class_='kbcontent1')
            if len(course_info) > 0:
                course_info = str(course_info[0]).replace('<div class="kbcontent1" id="">', '')
                course_info = str(course_info).replace('</div>', '')
                course_info = str(course_info).replace('<br/>', '\n')
                print(course_info)

            else:
                course_info = "此时间段无课程"
                print("此时间段无课程")

            day = int(cnt / 6)
            section = cnt % 6
            e.set_column(1, day + 1, 30)
            e.write(section + 1, day + 1, course_info, workfomat)
            print(day, section)
            print("==============")
            cnt = cnt + 1

    # 关闭 & 保存
    o.close()
    return path
