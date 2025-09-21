import re
import os

import requests
import json

from bs4 import BeautifulSoup # для поиска по html
import logging

# Включаем дебаг logging
logging.basicConfig(level=logging.DEBUG)

class Requests:
    def __init__(self, cookies_file='cookies.json'):
        self.session = requests.Session()
        self.cookies_file = cookies_file
        with open('headers_defualt.json', 'r') as head:
            self.headers = json.load(head)

        self.urlLoginPage = 'https://passport.yandex.ru/auth/add?origin=music&retpath=https%3A%2F%2Fmusic.yandex.ru%2F&language=ru'
        self.urlStartLoginRequest = 'https://passport.yandex.ru/registration-validations/auth/multi_step/start'
        self.urlSendPush = "https://passport.yandex.ru/registration-validations/auth-suggest-send-push"
        self.urlUserEntryFlowSubmit = 'https://passport.yandex.ru/registration-validations/user-entry-flow-submit'
        self.urlCheckPushCode = 'https://passport.yandex.ru/registration-validations/check-push-code'
        self.urlNeoPhonishAuth = "https://passport.yandex.ru/registration-validations/neo-phonish-auth"
        self.urlAuthAccounts = 'https://passport.yandex.ru/registration-validations/auth/accounts'
        
        self._load_cookies()

    def _load_cookies(self):
        """Загружаем куки из файла если есть"""
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r') as f:
                    cookies_dict = json.load(f)
                    self.session.cookies.update(cookies_dict)
                    print("Куки загружены из файла")
            except:
                print("Не удалось загрузить куки")

    def _save_cookies(self):
        """Сохраняем куки в файл"""
        try:
            with open(self.cookies_file, 'w') as f:
                json.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
            print("Куки сохранены в файл")
        except Exception as e:
            print(f"Ошибка сохранения куки: {e}")

    def getCustom(self,url:str):
        response = self.session.get(url,headers=self.headers)
        self._save_cookies()
        return response

    def postCustom(self,url:str, data:dict={}):
        response = self.session.post(
            url,
            headers=self.headers,
            data=data
        )
        self._save_cookies()
        return response

    
    def search_in_html(self, html):
        """Посик csrf и uuid на странице полученный от get запрса"""
        soup = BeautifulSoup(html, 'lxml')

        token_csrf = soup.find('input', {'name': 'csrf_token'})
        if token_csrf:
            csrf = token_csrf.get('value')
        
        for link in soup.find_all('a', href=True):
            match = re.search(r'process_uuid=([a-f0-9-]+)', link['href'])
            if match:
                uuid = match.group(1)
    
        return [csrf, uuid]

    def login():
        """функция для входа в аккаунт, потребует потом смс код"""
        

if __name__ == "__main__":
    api = Requests()
    response = api.get_easy('https://passport.yandex.ru/auth?origin=music&language=ru')
    print(api.search_in_html(response))

