import re
import logging

import urllib.request  # Для запросов
import urllib.parse    # Для кодирования данных
import http.cookiejar  # Для работы с куками 

from bs4 import BeautifulSoup # для поиска по html

class Requests:
    def __init__(self):
        pass

    def get_easy(self,url:str):
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        return html
    
    def search_in_html(self, html, token):
        soup = BeautifulSoup(html, 'lxml')
        token_input = soup.find('input', {'name': token})
        if token_input:
            return token_input.get('value')
        
        for link in soup.find_all('a', href=True):
            match = re.search(r'process_uuid=([a-f0-9-]+)', link['href'])
            if match:
                return match.group(1)
        return None

if __name__ == "__main__":
    api = Requests()
    api.get_easy('https://passport.yandex.ru/auth?origin=music&language=ru')