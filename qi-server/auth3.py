import base64

import requests
from pyDes import des, ECB, PAD_PKCS5


class Auth:
    cookies = {}
    ok = False

    def __init__(self, cookies=None):
        self.session = requests.session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ' \
                                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        self.session.headers['Host'] = 'auth.sztu.edu.cn'
        self.session.headers['Referer'] = 'https://auth.sztu.edu.cn/idp/authcenter/ActionAuthChain?entityId=jiaowu'
        self.session.headers['Origin'] = 'https://auth.sztu.edu.cn'
        self.session.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.session.headers['Sec-Fetch-Site'] = 'same-origin'
        self.session.headers['Sec-Fetch-Mode'] = 'cors'
        self.session.headers['Sec-Fetch-Dest'] = 'empty'
        self.session.headers['sec-ch-ua-mobile'] = '?0'
        self.session.headers['sec-ch-ua-platform'] = '"macOS"'
        self.session.headers['sec-ch-ua'] = '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"'
        self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        if cookies:
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
            self.check_login()

    def login(self, school_id, password):
        # 初始化 session
        self.session.headers['Host'] = 'jwxt.sztu.edu.cn'
        resp = self.session.get('https://jwxt.sztu.edu.cn/', allow_redirects=False, verify=False)
        # 1
        resp = self.session.get(resp.headers['Location'], allow_redirects=False)
        # 2
        resp = self.session.get(resp.headers['Location'], allow_redirects=False)

        self.session.headers['Host'] = 'auth.sztu.edu.cn'
        self.session.get(resp.headers['Location'], allow_redirects=False)

        self.session.get('https://auth.sztu.edu.cn/idp/AuthnEngine', allow_redirects=False)
        self.session.get('https://auth.sztu.edu.cn/idp/authcenter/ActionAuthChain?entityId=jiaowu')
        # 构造登录
        data = {
            'j_username': school_id,
            'j_password': self.encryptByDES(password),
            'j_checkcode': '验证码',
            'op': 'login',
            'spAuthChainCode': 'cc2fdbc3599b48a69d5c82a665256b6b'
        }
        resp = self.session.post('https://auth.sztu.edu.cn/idp/authcenter/ActionAuthChain',
                                 data=data, allow_redirects=False)
        resp = resp.json()
        # print(resp)
        if resp['loginFailed'] != 'false':
            return {}, False

        resp = self.session.post('https://auth.sztu.edu.cn/idp/AuthnEngine?'
                                 'currentAuth=urn_oasis_names_tc_SAML_2.0_ac_classes_BAMUsernamePassword',
                                 data=data, allow_redirects=False)
        ssoURL = resp.headers['Location']
        resp = self.session.get(ssoURL, allow_redirects=False)
        logonUrl = resp.headers['Location']

        self.session.headers['Host'] = 'jwxt.sztu.edu.cn'
        resp = self.session.get(logonUrl, allow_redirects=False)
        loginToTkUrl = resp.headers['Location']
        self.session.get(loginToTkUrl, allow_redirects=False)
        self.session.get('https://jwxt.sztu.edu.cn/jsxsd/framework/xsMain.htmlx')
        self.cookies = self.session.cookies.get_dict()

        self.check_login()

        return self.cookies, self.ok

    @staticmethod
    def encryptByDES(message):
        secret_key = 'PassB01Il71'[0:8]  # 密钥
        iv = secret_key  # 偏移
        # secret_key:加密密钥，EBC:加密模式，iv:偏移, padmode:填充
        des_obj = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
        # 返回为字节
        secret_bytes = des_obj.encrypt(message, padmode=PAD_PKCS5)
        # 返回为base64
        return base64.b64encode(secret_bytes)

    def check_login(self):
        resp = self.session.get('https://jwxt.sztu.edu.cn/jsxsd/framework/xsMain.htmlx')
        self.ok = (resp.status_code == 200)

    def get(self, url):
        return self.session.get(url, timeout=2, cookies=self.cookies, verify=False)

    def get_excel(self, url):
        headers = self.session.headers
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,' \
                            'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        return self.session.get(url, headers=headers, timeout=2, cookies=self.cookies, verify=False)

    def post(self, url, data):
        return self.session.post(url, timeout=2, cookies=self.cookies, verify=False, data=data)
