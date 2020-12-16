import requests
from config import config

# 登录


class Auth:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.83 Safari/537.36',
        'Host': 'isea.sztu.edu.cn'
    }

    host = 'https://isea.sztu.edu.cn'

    session = requests.session()

    def __init__(self):
        self.get_cookie()
        self.login()

    def encode(self, username, password):
        url = '/Logon.do?method=logon&flag=sess'
        r = self.session.get(self.host + url, headers=self.headers)
        data_str = r.text
        scode = data_str.split("#")[0]
        sxh = data_str.split("#")[1]
        code = username + "%%%" + password
        encode = ""
        i = 0
        while i < len(code):
            if i < 20:
                encode += code[i:i + 1] + scode[0:int(sxh[i:i + 1])]
                scode = scode[int(sxh[i:i + 1]):len(scode)]
            else:
                encode += code[i:len(code)]
                i = len(code)
            i += 1
        return encode

    def login(self):
        url = '/Logon.do?method=logon'
        name = config.get('user', 'name')
        pwd = config.get('user', 'password')
        data = {
            'encoded': self.encode(name, pwd)
        }

        r = self.session.post(self.host+url, headers=self.headers, data=data)
        if '培养方案' in r.text:
            print('登录成功')
        else:
            print(r.text)
            print('登录失败')

    def get_cookie(self):
        self.session.get(self.host, headers=self.headers)
        return self.session
