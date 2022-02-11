from bs4 import BeautifulSoup

from auth3 import Auth


def get_semester(cookies):
    auth = Auth(cookies)
    r = auth.get('https://jwxt.sztu.edu.cn/jsxsd/xskb/xskb_list.do')
    soup = BeautifulSoup(r.text, features='html.parser')
    options = soup.find('select', id='xnxq01id')
    # [<option selected="selected" value="2021-2022-1">2021-2022-1</option>]
    selected = options.findAll('option', attrs={'selected': 'selected'})[0].getText()
    options = options.findAll('option')
    semester = []
    for option in options:
        semester.append(option.getText())

    return semester, selected
