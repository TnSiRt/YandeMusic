from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton

from ui.convetor import hex_to_rgba
import json

from kivymd.app import MDApp 

with open("config.json",'r') as f:
    color_schem = json.load(f)

class BtnSoundControlHorizantal(MDGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cols=3
        self.rows=1
        self.app = MDApp.get_running_app()

        self.leftBtn = MDAnchorLayout(anchor_x='center',anchor_y='center')
        self.skipPreviousBtn = MDIconButton(
            icon='skip-previous-circle-outline',
            icon_color=hex_to_rgba(color_schem['playerBtn']),
            theme_icon_color='Custom',
            font_size=35,
            theme_font_size="Custom",
            on_release=self.prevCallback
        )
        self.leftBtn.add_widget(self.skipPreviousBtn)

        self.centerBtn = MDAnchorLayout(anchor_x='center',anchor_y='center')
        self.pauseUnpauseBtn = MDIconButton(
            icon='play-circle-outline',
            icon_color=hex_to_rgba(color_schem['playerBtn']),
            theme_icon_color='Custom',
            font_size=35,
            theme_font_size="Custom",
            on_release = lambda x: self.playPause(change=False)
        )
        self.centerBtn.add_widget(self.pauseUnpauseBtn)

        self.rightBtn = MDAnchorLayout(anchor_x='center',anchor_y='center')
        self.skipNextBtn = MDIconButton(
            icon='skip-next-circle-outline',
            icon_color=hex_to_rgba(color_schem['playerBtn']),
            theme_icon_color='Custom',
            font_size=35,
            theme_font_size="Custom",
            on_release=self.nextCallback
        )
        self.rightBtn.add_widget(self.skipNextBtn)

        self.add_widget(self.leftBtn)
        self.add_widget(self.centerBtn)
        self.add_widget(self.rightBtn)
    
    def nextCallback(self, *args):
        data = self.app.playListManager.next()
        index = self.app.playListManager.index
        self.app.playerScreen.children[0].children[0].setData(data, index)
    
    def prevCallback(self, *args):
        data = self.app.playListManager.prev()
        index = self.app.playListManager.index
        self.app.playerScreen.children[0].children[0].setData(data, index)


    def playPause(self, change:bool=False, *args):
        try:
            if change == False:
                if self.pauseUnpauseBtn.icon == 'play-circle-outline':  
                    self.pauseUnpauseBtn.icon = 'pause-circle-outline'
                    self.app.audioDriver.unpauseOrPlay()
                    self.app.playerScreen.children[0].children[0].stopOrStartEvent()
                else:
                    self.pauseUnpauseBtn.icon = 'play-circle-outline'
                    self.app.audioDriver.pause()
                    self.app.playerScreen.children[0].children[0].stopOrStartEvent()
            elif change == True:
                if self.pauseUnpauseBtn.icon == 'play-circle-outline':  
                    self.pauseUnpauseBtn.icon = 'pause-circle-outline'
        except Exception:
            index = self.app.playListManager.index
            data = self.app.playListManager.getAllInfoByCurrentIndex()
            self.app.playerScreen.children[0].children[0].setData(data, index)
            self.playPause()