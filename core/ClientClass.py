import re
import os

import requests
import json

from bs4 import BeautifulSoup # для поиска по html
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='yandex_debug.log',  # ← вот это важно
    filemode='w',  # 'w' - перезаписывать, 'a' - дописывать
    format='%(asctime)s - %(levelname)s - %(message)s'
)

config_path = os.path.join(os.path.dirname(__file__), 'headers_default.json')
token_path = os.path.join(os.path.dirname(__file__), 'tokens.json')

class Requests:
    def __init__(self, cookies_file='cookies.json'):
        self.session = requests.Session()
        self.cookies_file = cookies_file
        self.csrf = None
        self.uuid = None
        self.uid = None
        self.ncrnd = 66666
        with open(config_path, 'r') as head:
            self.headers = json.load(head)

        self.urlLoginPage = 'https://passport.yandex.ru/auth/add?origin=music&retpath=https%3A%2F%2Fmusic.yandex.ru%2F&language=ru'
        self.urlStartLoginRequest = 'https://passport.yandex.ru/registration-validations/auth/multi_step/start'
        self.urlSendPush = "https://passport.yandex.ru/registration-validations/auth-suggest-send-push"
        self.urlUserEntryFlowSubmit = 'https://passport.yandex.ru/registration-validations/user-entry-flow-submit'
        self.urlFindAccountsByPhoneV2 = 'https://passport.yandex.ru/registration-validations/find-accounts-by-phone-v2'
        self.urlCheckPushCode = 'https://passport.yandex.ru/registration-validations/check-push-code'
        self.urlNeoPhonishAuth = "https://passport.yandex.ru/registration-validations/neo-phonish-auth"
        self.urlAuthAccounts = 'https://passport.yandex.ru/registration-validations/auth/accounts'
        self.urlGetCommonTrack = 'https://passport.yandex.ru/registration-validations/getCommonTrack'
        self.urlAskV2 = 'https://passport.yandex.ru/registration-validations/auth/additional_data/ask_v2'
        
        self._load_cookies()

    def _load_cookies(self):
        """Загружаем куки из файла если есть"""
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r') as f:
                    cookies_dict = json.load(f)
                    self.session.cookies.update(cookies_dict)
                    try:
                        self.csrf = self.get_token('csrf')
                        self.uuid = self.get_token('uuid')
                        print("Куки загружены из файла")
                    except Exception as e:
                        logging.debug('Не удалось подгрузить токен')
                        print("[!]  Куки загружены из файла")
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

    def request(self, method, url, headers_key="base_headres_0", **kwargs):
        """Универсальный запрос с возможностью доп headers"""
        base_headers = {**self.headers[headers_key]}
        custom_headers = kwargs.pop('headers', {})  # Вытаскиваем если передали
        headers = {**base_headers, **custom_headers}

        kwargs['headers'] = headers
        response = self.session.request(method, url, **kwargs)
        self._save_cookies()
        return response

    def getCustom(self, url, headers_key="base_headres_0", **kwargs):
        return self.request('GET', url, headers_key, **kwargs)

    def postCustom(self, url, data=None, headers_key="base_headres_0", **kwargs):
        kwargs['data'] = data
        return self.request('POST', url, headers_key, **kwargs)

    
    def search_in_html(self, html):
        """Посик csrf и uuid на странице полученный от get запрса"""
        soup = BeautifulSoup(html, 'lxml')

        token_csrf = soup.find('input', {'name': 'csrf_token'})
        if token_csrf:
            csrf = token_csrf.get('value')
        
        retpath = soup.find('input', {"name":"retpath"})
        if retpath:
            url = retpath.get('value')

        for link in soup.find_all('a', href=True):
            match = re.search(r'process_uuid=([a-f0-9-]+)', link['href'])
            if match:
                uuid = match.group(1)
    
        return [csrf, uuid, url]

    def convert(self,**kwargs):
        """Конвертирует именованные параметры в dict"""
        return kwargs
    
    def get_user_id(self):
        """Получаем ID текущего пользователя"""
        response = self.getCustom("https://api.music.yandex.net/account/status")
        if response.status_code == 200:
            data = response.json()
            return data['result']['account']['uid'], data
        return None

    def get_liked_tracks(self, user_id):
        """Получаем список любимых треков"""
        url = f"https://api.music.yandex.net/users/{user_id}/likes/tracks"
        response = self.getCustom(url)
        
        if response.status_code == 200:
            return response.json()
        return None

    def add_token(self, name, value):
        with open(token_path, 'r') as file:
            data = json.load(file)
        file.close()

        data[name] = value

        with open(token_path,'w') as file:
            file.write(
                json.dumps(
                    data,
                    indent=4,
                    ensure_ascii=False
                )
            )
    
    def get_token(self, name):
        with open(token_path, 'r') as file:
            data = json.load(file)
        return data[name]
    
    def update_cookie(self):
        self.url_0 = f'https://sso.passport.yandex.ru/prepare?uuid={self.get_token('uuid')}&goal=https://ya.ru/&finish=https://music.yandex.ru/?ncrnd={self.ncrnd}'
        self.url_1 = f'https://sso.ya.ru/sync?uuid={self.get_token('uuid')}&finish=https://music.yandex.ru/?ncrnd=P{self.ncrnd}'
        
        self.postCustom(self.url_0)
        self.postCustom(self.url_1)
        self.getCustom(f"https://music.yandex.ru/?ncrnd={self.ncrnd}")

    def update_csrf(self):
        response = self.postCustom(
            self.urlAuthAccounts,
            data=self.convert(
                csrf_token=self.get_token('csrf'),
                origin='music'
            ),
            headers=self.headers['passport_1']
        )
        data = response.json()
        self.add_token('csrf',data['csrf'])

    def getLikePlayListUuid(self):
        self.update_cookie()
        uuid_playlist=self.getCustom('https://api.music.yandex.ru/landing-blocks/collection/playlist-with-likes')
        uuid = uuid_playlist.json()['result']['playlist']['playlistUuid']
        self.add_token('uuid_playlist',uuid)

    def getLikeListSond(self):
        self.update_cookie()
        response = self.getCustom(f"https://api.music.yandex.ru/playlist/{self.get_token('uuid_playlist')}?resumeStream=false&richTracks=false")
        data = response.json() 
        print(data['result']['title'])

    def login(self):
        """функция для входа в аккаунт, потребует потом смс код"""
        number = input("номер >> ")
        response = self.getCustom(self.urlLoginPage)
        csrf, uuid, retpath = self.search_in_html(response.text)
        self.add_token('csrf',csrf)
        self.add_token('uuid', uuid)

        response = self.postCustom(
            self.urlStartLoginRequest,
            data=self.convert(
                csrf_token=csrf,
                login=number,
                process_uuid=uuid,
                retpath=retpath,
                origin="music",
                check_for_xtokens_for_pictures="1",
                can_send_push_code="1",
                is_sms_auth_experiment="1",
                is_master_experiment="1",
                force_check_for_protocols="true"
            ),
            headers=self.headers['passport_0'],
        )
        track_id = response.json()['track_id']
        
        response = self.postCustom(
            self.urlSendPush,
            data=self.convert(
                csrf_token=csrf,
                track_id=track_id,
                phone_number=number,
                force_show_code_in_notification="1",
                can_use_anmon="true",
                isSilent2faPushesEnabled="true"
            ),
            headers=self.headers['passport_1']
        )
        data_json = response.json()
        print(data_json)
        if data_json['apps_for_bright_push'][0]['platform'] == 'ios':
            platform = 'iphone'

        
        response = self.postCustom(
            self.urlUserEntryFlowSubmit,
            data=self.convert(
                csrf_token=csrf,
                process="ENTRY_REGISTER_NEOPHONISH",
                origin="music",
                isSimplifiedPhoneAuth="false",
                process_uuid=uuid,
                track_id=track_id
            ),
            headers=self.headers['passport_0']
        )
        if response.json()['status'] == 'ok':
            print(f'проверьте ваш {platform}')
        


        self.postCustom(
            self.urlAuthAccounts,
            data=self.convert(
                csrf_token=csrf,
                origin="music"
            ),
            headers=self.headers['passport_0']
        )

        self.postCustom(
            self.urlCheckPushCode,
            data=self.convert(	
                csrf_token=csrf,
                track_id=track_id,
                code=input('push code >> ')
            ),
            headers=self.headers['passport_0']
        ) # send push to server

        response = self.postCustom(
            self.urlFindAccountsByPhoneV2,
            data=self.convert(
                csrf_token=csrf,
                track_id=track_id,
                can_use_anmon="true"
            )
        )
        data=response.json()
        uid=data['accounts'][0]['uid']
        self.add_token('uid', uid)
        print(data['accounts'][0]['display_name']['name'])

        self.postCustom(
            self.urlNeoPhonishAuth,
            data=self.convert(
                csrf_token=csrf,
                track_id=track_id,
                uid=uid,
                useNewSuggestByPhone="true",
                retpath=f"https://sso.passport.yandex.ru/prepare?uuid={uuid}&goal=https%3A%2F%2Fya.ru%2F&finish=https%3A%2F%2Fmusic.yandex.ru%2F",
                retpathWasEnhanced="false"
            ),
            headers=self.headers['passport_0']
        )

        response = self.postCustom(
            self.urlAuthAccounts,
            data=self.convert(
                csrf_token=csrf,
                origin='music'
            ),
            headers=self.headers['passport_1']
        )
        self.add_token('csrf',response.json()['csrf'])
        self.postCustom(
            self.urlGetCommonTrack,
            data=self.convert(
                csrf_token=csrf,
                origin="music",
                track_id=""
            ),
            headers=self.headers['passport_1']
        )
        self.postCustom(
            self.urlAskV2,
            data=self.convert(
                csrf_token=csrf,
                origin="music",
                track_id=track_id
            ),
            headers=self.headers['passport_1']
        )
        self.getCustom(
            'https://api.passport.yandex.ru/registration_status/check',
            headers_key='base_headres_1',
            headers=self.headers['api_passport_0']
        )
        response = self.postCustom(
            self.urlAuthAccounts,
            data=self.convert(
                csrf_token=csrf,
                origin='music'
            ),
            headers=self.headers['passport_1']
        )
        self.add_token('csrf',response.json()['csrf'])

if __name__ == "__main__":
    api = Requests()
    api.getLikeListSond()
    


