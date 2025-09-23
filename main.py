import os

from kivy.core.window import Window
from concurrent.futures import ThreadPoolExecutor

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from core.ClientClass import Requests

from ui.PlayerScreen import Player
from ui.LoginScreen import Login

from core.audioDriver import AudioDriver
from core.playlistManager import PlayListManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MyApp(MDApp):

    def build(self):
        #api для запросов
        self.api = Requests()
        self.executor = ThreadPoolExecutor(max_workers=4) 
        self.audioDriver = AudioDriver()
        self.playListManager = PlayListManager()
        # минимальные размеры
        Window.minimum_width = 1300
        Window.minimum_height = 800

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"  # "Purple", "Red"

        self.sm = MDScreenManager()
        if self.api.client == None:
            self.sm.add_widget(Login(api=self.api, changeFunc=self.changeScreen))
        else:
            data = self.api.get_cash()
            if data == {}:
                pass
            else:
                dataPlayList = []
                for i in data:
                    dataPlayList.append(data[i])
                self.playListManager.load(dataPlayList)
        self.playerScreen = Player(api=self.api)
        self.sm.add_widget(self.playerScreen)

        return self.sm

    def reloadCash(self):
        data = self.api.get_cash()
        dataPlayList = []
        for i in data:
            dataPlayList.append(data[i])
        self.playListManager.load(dataPlayList)

    def changeScreen(self,name):
        self.sm.current = name


if __name__ == '__main__':
    MyApp().run()
 