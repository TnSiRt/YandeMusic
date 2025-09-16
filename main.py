import os

from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from ui.PlayerScreen import Player

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



class MyApp(MDApp):

    def build(self):
        # минимальные размеры
        Window.minimum_width = 1300
        Window.minimum_height = 800

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"  # "Purple", "Red"

        self.sm = MDScreenManager()
        self.sm.add_widget(Player())

        return self.sm


if __name__ == '__main__':
    MyApp().run()
 