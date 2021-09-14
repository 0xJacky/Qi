import datetime
from time import sleep

import requests
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

urllib3.disable_warnings()


class Auth:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 Safari/537.36',
        'Host': 'jwxt.sztu.edu.cn'
    }

    ok = False

    cookies = {}

    def __init__(self, cookies=None):
        if cookies is not None:
            self.cookies = cookies
            self.check_login()

    def login(self, username, password):
        start = datetime.datetime.now()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://auth.sztu.edu.cn/idp/authcenter/ActionAuthChain?entityId=jiaowu')

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'loginButton'))
            )

            driver.find_element_by_name('j_username').send_keys(username)
            driver.find_element_by_name('j_password').send_keys(password)

            driver.find_element_by_id('loginButton').click()

            sleep(1)

            try:
                Alert(driver).dismiss()
            except Exception as e:
                print(e)

            # driver.get('https://jwxt.sztu.edu.cn/jsxsd/framework/xsMain.jsp#')

            print(driver.get_cookies())

            cookies = driver.get_cookies()

            for cookie in cookies:
                self.cookies[cookie['name']] = cookie['value']

            # 改 self.ok 标志位
            self.check_login()

        finally:
            driver.quit()

        print(self.cookies)
        end = datetime.datetime.now()
        print('登录用时', (end - start).microseconds, 'ms')
        return self.cookies, self.ok

    def check_login(self):
        r = self.get('https://jwxt.sztu.edu.cn/jsxsd/framework/xsMain_new.jsp?t1=1')
        self.ok = '教学进程' in r.text

    def get(self, url):
        return requests.get(url, headers=self.headers, timeout=2, cookies=self.cookies, verify=False)

    def get_excel(self, url):
        headers = self.headers
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,' \
                            'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        return requests.get(url, headers=headers, timeout=2, cookies=self.cookies, verify=False)

    def post(self, url, data):
        return requests.post(url, headers=self.headers, timeout=2, cookies=self.cookies, verify=False, data=data)
