from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton

from ui.convetor import hex_to_rgba
import json

with open("config.json",'r') as f:
    color_schem = json.load(f)

class BtnSoundControlHorizantal(MDGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cols=3
        self.rows=1

        self.leftBtn = MDAnchorLayout(anchor_x='center',anchor_y='center')
        self.skipPreviousBtn = MDIconButton(
            icon='skip-previous-circle-outline',
            icon_color=hex_to_rgba(color_schem['playerBtn']),
            theme_icon_color='Custom',
            font_size=35,
            theme_font_size="Custom"
        )
        self.leftBtn.add_widget(self.skipPreviousBtn)

        self.centerBtn = MDAnchorLayout(anchor_x='center',anchor_y='center')
        self.pauseUnpauseBtn = MDIconButton(
            icon='play-circle-outline',
            icon_color=hex_to_rgba(color_schem['playerBtn']),
            theme_icon_color='Custom',
            font_size=35,
            theme_font_size="Custom"
        )
        self.centerBtn.add_widget(self.pauseUnpauseBtn)

        self.rightBtn = MDAnchorLayout(anchor_x='center',anchor_y='center')
        self.skipNextBtn = MDIconButton(
            icon='skip-next-circle-outline',
            icon_color=hex_to_rgba(color_schem['playerBtn']),
            theme_icon_color='Custom',
            font_size=35,
            theme_font_size="Custom"
        )
        self.rightBtn.add_widget(self.skipNextBtn)

        self.add_widget(self.leftBtn)
        self.add_widget(self.centerBtn)
        self.add_widget(self.rightBtn)