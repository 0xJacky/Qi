import datetime
import time

import requests
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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

    def __init__(self, username, password):
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

        driver.find_element_by_name('j_username').send_keys(username)
        driver.find_element_by_name('j_password').send_keys(password)

        driver.find_element_by_id('loginButton').click()

        time.sleep(1)

        driver.get('https://jwxt.sztu.edu.cn/jsxsd/framework/xsMain.jsp#')

        print(driver.get_cookies())

        cookies = driver.get_cookies()

        for cookie in cookies:
            self.cookies[cookie['name']] = cookie['value']

        self.ok = '培养管理' in driver.page_source

        driver.quit()
        print(self.cookies)
        end = datetime.datetime.now()
        print('login use', (end - start).microseconds, 'ms')

    def get(self, url):
        return requests.get(url, headers=self.headers, timeout=2, cookies=self.cookies, verify=False)