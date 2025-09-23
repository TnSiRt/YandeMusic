import json
from kivy.graphics import Color, Line
from kivy.clock import Clock
from kivy.animation import Animation

from kivymd.app import MDApp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.anchorlayout import MDAnchorLayout

from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton

from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemLeadingAvatar, MDListItemSupportingText
from kivymd.uix.scrollview import MDScrollView

from kivymd.uix.slider import MDSlider, MDSliderHandle
from kivymd.uix.divider import MDDivider
from kivymd.uix.progressindicator import MDCircularProgressIndicator

from kivymd.uix.screen import MDScreen
from ui.convetor import hex_to_rgba, ms_to_time, s_to_time
from ui.btn_layout import BtnSoundControlHorizantal

from core.audioDriver import AudioDriver

with open("config.json",'r') as f:
    color_schem = json.load(f)

class DataView(MDGridLayout):
    def __init__(self,api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        self.api = api
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
    
        self.app.executor.submit(self._loading)

    def _loading(self):
        if self.api.get_cash() == {}:
            self.api.getLikeSound()
            self._isLoadData = False
        else:
            pass
        self._isLoadData = False
        Clock.schedule_once(lambda dt: self.init_load_treack(), 0)

    def setTreack(self, i):
        self.app.playListManager.setIndex(int(i))
        data = self.app.playListManager.getAllInfoByCurrentIndex()
        self.app.playerScreen.children[0].children[0].setData(data, i)

    def init_load_treack(self):
        if self._isLoadData:
           self.likeSoundBox.add_widget(self.loadTreackIndicatorBox)
        else:
           self.likeSoundBox.remove_widget(self.loadTreackIndicatorBox)
           for i in self.api.get_treack_by_id():
               data = self.api.get_treack_by_id(str(i))
               self.item = MDListItem(
                    MDListItemLeadingAvatar(
                        source=f'http://{data['image'].replace("%%","100x100")}',
                    ),
                    MDListItemHeadlineText(
                        text=data['title'],
                    ),
                    MDListItemSupportingText(
                        text=data['artist'],
                    ),
               )
               self.item.on_release = lambda i=i: self.setTreack(i)
               self.listView.add_widget(self.item)
           self.likeSoundBox.add_widget(self.listViewTreack)

class ControlUI(MDGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cols = 3
        self.rows = 1
        self.padding = [10,10]
        self.app = MDApp.get_running_app()
        self.updateEventProgressbar = None

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
        self.progressTreack = MDSlider(
            track_active_color=hex_to_rgba(color_schem['playerProgressBar']),
            on_touch_move=self._setPosTreack
        )
        self.progressTreack.add_widget(MDSliderHandle())
        self.totalTime = MDLabel(text='00:00', size_hint_x=0.2, halign='center') 

        self.controlBox.add_widget(self.currentTime)
        self.controlBox.add_widget(self.progressTreack)
        self.controlBox.add_widget(self.totalTime)
        self.dataBox.add_widget(self.controlBox)

        self.add_widget(self.dataBox)
        self.btnLayout= BtnSoundControlHorizantal(
                size_hint_x=0.15
            )
        self.add_widget(
            self.btnLayout
        )

    def _set_new_background(self, *args):
        # подменяем картинку
        self.viewImage.reload()
        # включаем плавное появление
        Animation(opacity=1, duration=0.5).start(self.viewImage)
    
    def _setPosTreack(self, instance, value, *args):
        self.app.audioDriver.muiscDriver.play(start=instance.value)

    def stopOrStartEvent(self):
        if self.updateEventProgressbar == None:
            self.updateEventProgressbar = Clock.schedule_interval(self.updateProgressbar, 1)
        else:
            self.updateEventProgressbar.cancel()
            self.updateEventProgressbar = None

    def updateProgressbar(self, *args):
        self.currentTime.text = s_to_time(self.progressTreack.value)
        if int(self.progressTreack.value) != self.progressTreack.max:
            self.progressTreack.value += 1
        if int(self.progressTreack.value) == self.progressTreack.max:
            self.app.playerScreen.children[0].children[0].btnLayout.nextCallback(1)

    def resetUpdate(self):
        self.progressTreack.value = 0
        self.currentTime.text = "00:00"
        if self.updateEventProgressbar != None: 
            self.updateEventProgressbar.cancel()
        self.updateEventProgressbar = Clock.schedule_interval(self.updateProgressbar, 1)

    def update_line(self, *args):
        """Обновляет линию при изменении размера"""
        x1, y1 = self.x, self.top
        x2, y2 = self.right, self.top
        self.top_line.points = [x1, y1, x2, y2]
    
    def setData(self, data, i):
        self.index = i  # сохраняем выбранный индекс трека
        self.viewImage.source = data['image']
        self.progressTreack.max = ms_to_time(data['duration'],'sec')
        self.totalTime.text = ms_to_time(data['duration'])

        if data['file'] is None:
            # запускаем анимацию загрузки
            if hasattr(self, "_anim_event"):
                self._anim_event.cancel()
            self._anim_event = Clock.schedule_interval(self._animTextForDownload, 0.5)
            self.resetUpdate()
            self.stopOrStartEvent()
            # качаем в фоне
            self.app.audioDriver.pause()
            self.app.executor.submit(self._downloadFileWithInfoOfScreen, i)
        else:
            self.resetUpdate()
            self.titleAndArtist.text = f"{data['title']} - {data['artist']}"
            self.app.audioDriver.load(f"{data['title'].replace(' ', '_')}_{data['artist'].replace(' ', '_')}.mp3")
            self.app.audioDriver.unpauseOrPlay()
            self.btnLayout.playPause(change=True)

        self.app.reloadCash()


    def _downloadFileWithInfoOfScreen(self, i):
        self.app.api.downloadFileChoisse(str(i))        
        Clock.schedule_once(lambda dt: self._onDownloadFinished(i))

    def _onDownloadFinished(self, i):
        if hasattr(self, "_anim_event"):
            self._anim_event.cancel()
        data = self.app.playListManager.getAllInfoByCurrentIndex()
        self.setData(data, i)


    def _animTextForDownload(self, dt):
        labels = [
            "Download .",
            "Download ..",
            "Download ...",
            "Download ...."
        ]
        if not hasattr(self, "_anim_index"):
            self._anim_index = 0

        self.titleAndArtist.text = labels[self._anim_index % len(labels)]
        self._anim_index += 1

class Player(MDScreen):
    def __init__(self, api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Player'
        self.api = api
        self.md_bg_color = hex_to_rgba(color_schem['playerBackground'])

        self.main_box = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=[15,15]
        ) # главный контейнер всего экрана

        self.ContentView = DataView(api=self.api) # отбражениe списков и др.
        self.main_box.add_widget(self.ContentView)

        self.uiControl = ControlUI(
            md_bg_color=hex_to_rgba(color_schem['playerLine']),
            size_hint_y=0.3,
            size_hint_max_y=120
        ) # отбражение управления и информации
        self.main_box.add_widget(self.uiControl)

        self.add_widget(self.main_box)
