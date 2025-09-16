import json
from kivy.graphics import Color, Line

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.anchorlayout import MDAnchorLayout

from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton

from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemLeadingAvatar
from kivymd.uix.scrollview import MDScrollView

from kivymd.uix.slider import MDSlider
from kivymd.uix.divider import MDDivider
from kivymd.uix.progressindicator import MDCircularProgressIndicator

from kivymd.uix.screen import MDScreen
from ui.convetor import hex_to_rgba
from ui.btn_layout import BtnSoundControlHorizantal

with open("config.json",'r') as f:
    color_schem = json.load(f)

class DataView(MDGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cols = 2
        self.rows = 1
        # self.padding = [0,10]
        self.spacing = 10
        self._isLoadData = True

        self.likeSoundBox = MDGridLayout(
            cols=1,
            rows=3,
            spacing=5,
            size_hint_x=0.35,
            md_bg_color=hex_to_rgba(color_schem['playerContentView'])
        )


        self.layoutLblF = MDAnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint_y=0.1,
        )

        self.lblLike = MDLabel(
            text='Favorite',
            halign='center',
            font_style='Headline',
            role='large'
        )
        self.layoutLblF.add_widget(self.lblLike)
        self.likeSoundBox.add_widget(self.layoutLblF)

        self.divider = MDDivider(divider_width=10)
        self.likeSoundBox.add_widget(self.divider)

        # дальше нужно чуть пояснить, для тех кто будет рефакторить код
        # дальше будет создаваться два виджет без добавления, за отбражение будет отвечать специальная функция

        self.loadTreackIndicatorBox = MDFloatLayout() # добавить в likeSoundBox пока клиент ждет данные
        self.indicatorWidget = MDCircularProgressIndicator(
            determinate=True,
            size_hint=(None, None),
            size=("48dp", "48dp"),
            pos_hint={'center_x': .5, 'center_y': .5},
        )
        self.loadTreackIndicatorBox.add_widget(self.indicatorWidget)

        self.listViewTreack = MDScrollView()
        self.listView = MDList()
        self.listViewTreack.add_widget(self.listView)


        self.add_widget(self.likeSoundBox)

        self.searchSoundBox = MDGridLayout(
            cols=1,
            rows=3,
            spacing=10,
            md_bg_color=hex_to_rgba(color_schem['playerContentView'])
        )

        self.searchLineBox = MDBoxLayout(size_hint_y=0.10, padding=[10,0])
        
        self.layoutF = MDAnchorLayout(anchor_x='center', anchor_y='center')
        self.searchFiled = MDTextField(size_hint_y=0.65)
        self.layoutF.add_widget(self.searchFiled)
        self.searchLineBox.add_widget(self.layoutF)

        self.layoutBtn = MDAnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.1)
        self.startSearchBtn = MDIconButton(icon='magnify', style='filled')
        self.layoutBtn.add_widget(self.startSearchBtn)
        self.searchLineBox.add_widget(self.layoutBtn)

        self.searchSoundBox.add_widget(self.searchLineBox)

        self.lineDivider = MDDivider(size_hint_y=0.05)
        self.searchSoundBox.add_widget(self.lineDivider)

        self.boxResult = MDBoxLayout()

        self.viewListResult = MDLabel(
            text='Search ...',
            halign='center',
            font_style='Headline',
            role='large'
        )
        self.boxResult.add_widget(self.viewListResult)

        self.searchSoundBox.add_widget(self.boxResult)

        self.add_widget(self.searchSoundBox)
    
        self.init_load_treack()

    def init_load_treack(self):
        if self._isLoadData:
           self.likeSoundBox.add_widget(self.loadTreackIndicatorBox)
        else:
           self.likeSoundBox.add_widget(self.listViewTreack)

class ControlUI(MDGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cols = 3
        self.rows = 1
        self.padding = [10,10]

        with self.canvas.after:
            Color(0.60, 0.27, 0.0, 1)
            self.top_line = Line(points=[], width=1.5)

        self.bind(pos=self.update_line, size=self.update_line)


        self.viewImage = FitImage(
            source='ui/assets/image/test_albom.jpg',
            size_hint=(None,None),
            size=(100,100)
        )
        self.add_widget(self.viewImage)

        self.dataBox = MDBoxLayout(orientation='vertical')

        self.titleAndArtist = MDLabel(text='Title - Artist', halign='center')
        self.dataBox.add_widget(self.titleAndArtist)

        self.controlBox = MDBoxLayout()

        self.currentTime = MDLabel(text='00:00', size_hint_x=0.2, halign='center')
        self.progressTreack = MDSlider(track_active_color=hex_to_rgba(color_schem['playerProgressBar']))
        self.totalTime = MDLabel(text='00:00', size_hint_x=0.2, halign='center') 

        self.controlBox.add_widget(self.currentTime)
        self.controlBox.add_widget(self.progressTreack)
        self.controlBox.add_widget(self.totalTime)
        self.dataBox.add_widget(self.controlBox)

        self.add_widget(self.dataBox)
        self.add_widget(BtnSoundControlHorizantal(size_hint_x=0.15))
    
    def update_line(self, *args):
        """Обновляет линию при изменении размера"""
        x1, y1 = self.x, self.top
        x2, y2 = self.right, self.top
        self.top_line.points = [x1, y1, x2, y2]


class Player(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Player'
        self.md_bg_color = hex_to_rgba(color_schem['playerBackground'])

        self.main_box = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=[15,15]
        ) # главный контейнер всего экрана

        self.ContentView = DataView() # отбражениe списков и др.
        self.main_box.add_widget(self.ContentView)

        self.uiControl = ControlUI(
            md_bg_color=hex_to_rgba(color_schem['playerLine']),
            size_hint_y=0.3,
            size_hint_max_y=120
        ) # отбражение управления и информации
        self.main_box.add_widget(self.uiControl)

        self.add_widget(self.main_box)
