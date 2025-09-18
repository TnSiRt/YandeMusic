import requests
from bs4 import BeautifulSoup
import re
import json
import os

class YandexAuthParser:
    def __init__(self, cookies_file='cookies.json'):
        self.session = requests.Session()
        self.cookies_file = cookies_file
        self.headers = {
            "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            'accept-encoding': 'gzip, deflate, br',
            'origin': 'https://passport.yandex.ru',
            'referer': 'https://passport.yandex.ru/',
            'sec-ch-ua': '"Chromium";v="140", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-requested-with': 'XMLHttpRequest'
        }
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
    
    def get(self, url, **kwargs):
        """Обёртка для GET запроса с headers"""
        kwargs.setdefault('headers', self.headers)
        response = self.session.get(url, **kwargs)
        return response
    
    def post(self, url, data:dict=None, json:bool=False, **kwargs):
        """Обёртка для POST запроса с headers"""
        if json == False:
            kwargs.setdefault('headers', self.headers)
        else:
            headers = {
                **self.headers, 
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                "Accept":"application/json, text/javascript, */*; q=0.01"
            }
            kwargs.setdefault('headers',headers)
        if data == None:
            response = self.session.post(url, **kwargs)
        else:
            response = self.session.post(url, data=data, **kwargs)
        
        return response
    
    def get_tokens(self, data):
        """Получаем CSRF токен и Process UUID"""
        try:
            soup = BeautifulSoup(data, 'lxml')
            
            csrf_token = self._find_csrf_token(soup)
            process_uuid = self._find_process_uuid(soup)
            track_id = self._find_track_id(soup)
            
            return csrf_token, process_uuid, track_id
            
        except Exception as e:
            print(f"Ошибка при получении токенов: {e}")
            return None, None
    
    def _find_csrf_token(self, soup):
        """Ищем CSRF токен"""
        token_input = soup.find('input', {'name': 'csrf_token'}) or soup.find('input', {'name': 'csrf-token'})
        if token_input:
            return token_input.get('value')
        
        meta_token = soup.find('meta', {'name': 'csrf-token'})
        return meta_token.get('content') if meta_token else None
    
    def _find_process_uuid(self, soup):
        """Ищем Process UUID"""
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            match = re.search(r'process_uuid=([a-f0-9-]+)', href)
            if match:
                return match.group(1)
        
        return None

    def _find_track_id(self, soup):
        """Ищем CSRF токен"""
        token_input = soup.find('input', {'name': 'track_id'}) or soup.find('input', {'name': 'track-id'})
        if token_input:
            return token_input.get('value')
        
        meta_token = soup.find('meta', {'name': 'track-id'})
        return meta_token.get('content') if meta_token else None
    
    

# Пример использования
if __name__ == "__main__":
    api = YandexAuthParser()
    login_url = 'https://passport.yandex.ru/auth/welcome?origin=music&retpath=https%3A%2F%2Fmusic.yandex.ru&language=ru'

    response = api.get(login_url)
    csrf, uuid, track_id =  api.get_tokens(response.text)
    
    password = input("password >>")
    login = input("login >>")

    data = {
        "csrf_token":csrf,
        "track_id":track_id,
        "login":"patrionsPal",
        "process_uuid":uuid,
        "retpath":f"https://sso.passport.yandex.ru/prepare?uuid={uuid}&goal=https%3A%2F%2Fya.ru%2F&finish=https%3A%2F%2Fid.yandex.ru%2F",
        "origin":"music",
        "passwd":password
    }

    response = api.post(
        "https://passport.yandex.ru/registration-validations/auth/multi_step/start",
        data=data,
        json=True
    )
    json_data = response.json()
    track_id = json_data['track_id']

    data_step_2 = {
        'csrf_token':csrf,
        'track_id':track_id,
        'language':"ru"
    }

    data_step_4 = {
        'csrf_token':csrf,
        'track_id':track_id,
        'number':"+79524928490",
        'can_use_anmon':"true"
    }

    response = api.post(
        "https://passport.yandex.ru/registration-validations/check-phone-possibilities-v2",
        data=data_step_4,
        json=True
    )
    json_data = response.json()
    id_unknow = json_data['id']

    data_step_5 = {
        'csrf_token':csrf,
        'track_id':track_id,
        'validate_for_call':"true",
        'phone_number':"+79524928490",
        'validate_for_message_protocols':"true",
        'force_check_for_protocols':"true"
    }

    response = api.post(
        "https://passport.yandex.ru/registration-validations/validate-phone",
        data=data_step_5,
        json=True
    )
    json_data = response.json()
    print(f"{"-"*10}")
    print(json_data)

    data_step_6 = {
        'csrf_token':csrf,
        'track_id':track_id,
        'phone_number':"79524928490",
        'force_show_code_in_notification':"1",
        'can_use_anmon':"true",
        'isSilent2faPushesEnabled':"true"
    }

    response = api.post(
        "https://passport.yandex.ru/registration-validations/auth-suggest-send-push",
        data=data_step_6,
        json=True
    )
    json_data = response.json()
    print(f"{"-"*10}")
    print(json_data)


    data_step_7 = {
        'csrf_token':csrf,
        'process':"ENTRY_REGISTER_NEOPHONISH",
        'origin':"music",
        'isSimplifiedPhoneAuth':"false",
        'process_uuid':uuid,
        'track_id':track_id
    }

    response = api.post(
        "https://passport.yandex.ru/registration-validations/user-entry-flow-submit",
        data=data_step_7,
        json=True
    )
    json_data = response.json()
    print(f"{"-"*10}")
    print(json_data)

    code = input('code >> ')

    data_step_8 = {
        'csrf_token':csrf,
        'track_id':track_id,
        "code":code
    }

    response = api.post(
        "https://passport.yandex.ru/registration-validations/check-push-code",
        data=data_step_8,
        json=True
    )
    json_data = response.json()
    print(f"{"-"*10}")
    print(json_data)

    api._save_cookies()
