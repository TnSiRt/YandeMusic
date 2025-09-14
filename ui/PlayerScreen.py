from kivy.metrics import dp

from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.divider import MDDivider

from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.slider import MDSlider

from kivymd.uix.screen import MDScreen

class DataView(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.padding = [10,10]

        self.favorite_box = MDBoxLayout(orientation='vertical', size_hint_x=0.35)

        self.lbl = MDLabel(
            text='Любимое',
            size_hint_y=0.1,
            font_style='Display',
            role='small'
        )
        self.favorite_box.add_widget(self.lbl)
        self.favorite_box.add_widget(MDDivider(size_hint_y=0.05))

        self.box_indicator = MDFloatLayout()
        self.indicator = MDCircularProgressIndicator(
            size=("48dp", "48dp"),
            size_hint=(None, None),
            pos_hint={'center_x': .5, 'center_y': .5},
        )
        self.box_indicator.add_widget(self.indicator)

        self.favorite_box.add_widget(self.box_indicator)
 
        self.add_widget(self.favorite_box)

        self.add_widget(MDDivider(orientation='vertical',divider_width=5))

        self.search_box = MDBoxLayout(
            orientation='vertical', 
        )

        self.search_line = MDBoxLayout(spacing=20, size_hint_y=0.1, padding=[10,5])
        self.input_request = MDTextField(mode="outlined",size_hint_y=0.9)
        self.search_button = MDButton(
            MDButtonText(
                text="Search",
            ),
            style="filled",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        self.search_line.add_widget(self.input_request)
        self.search_line.add_widget(self.search_button)

        self.search_box.add_widget(self.search_line)

        self.search_box.add_widget(MDDivider())

        self.list_result = MDBoxLayout()
        self.list_result.add_widget(
            MDLabel(
                text='Result',
                font_style='Display', 
                role='small',
                halign='center'
            )
        )
        self.search_box.add_widget(self.list_result)        

        self.add_widget(self.search_box)


class ControlUI(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'vertical'
        self.padding = [10,5]

        self.top_box = MDBoxLayout()

        self.info_box = MDBoxLayout(spacing=20)
        self.view_image = FitImage(
            source='ui/assets/image/test_albom.jpg',
            size = (80, 80),
            size_hint= (None, None),
            radius=(dp(20), dp(20), dp(20), dp(20)),
            pos_hint={'center_x':0.5,"center_y":0.5}
        )

        self.title_and_artist = MDBoxLayout(orientation='vertical', padding=[0,10])
        self.title = MDLabel(text='Title')
        self.artist = MDLabel(text='Artist')

        self.title_and_artist.add_widget(self.title)
        self.title_and_artist.add_widget(self.artist)
        self.info_box.add_widget(self.view_image)
        self.info_box.add_widget(self.title_and_artist)

        self.btn_layout = MDBoxLayout(size_hint_x=0.35)

        self.layout = AnchorLayout(
            anchor_x='center', 
            anchor_y='center'
        )

        self.button_box = MDBoxLayout()

        self.prev_btn = MDIconButton(icon='skip-previous')
        self.play_pause_btn = MDIconButton(icon='play')
        self.next_btn = MDIconButton(icon='skip-next')

        self.button_box.add_widget(self.prev_btn)
        self.button_box.add_widget(self.play_pause_btn)
        self.button_box.add_widget(self.next_btn)

        self.top_box.add_widget(self.info_box)
        self.top_box.add_widget(MDBoxLayout())
        self.top_box.add_widget(self.btn_layout)
        self.btn_layout.add_widget(self.layout)
        self.layout.add_widget(self.button_box)

        self.add_widget(self.top_box)

        self.bottom_box = MDBoxLayout(size_hint_y=0.45)

        self.current_time = MDLabel(text='00:00', size_hint_x=0.2, halign='center')
        self.progress = MDSlider()
        self.total_time = MDLabel(text='00:00', size_hint_x=0.2, halign='center')

        self.bottom_box.add_widget(self.current_time)
        self.bottom_box.add_widget(self.progress)
        self.bottom_box.add_widget(self.total_time)

        self.add_widget(self.bottom_box)

class Player(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Player'

        self.main_box = MDBoxLayout(
            orientation='vertical',
            padding=[20,20],
            spacing=30
        ) # главный контейнер всего экрана

        self.ContentView = DataView() # отбражениe списков и др.
        self.cCard = MDCard()
        self.cCard.add_widget(self.ContentView)
        self.main_box.add_widget(self.cCard)

        self.uiControl = ControlUI() # отбражение управления и информации
        self.card = MDCard(size_hint_y=0.3, size_hint_max_y=150)
        self.card.add_widget(self.uiControl)
        self.main_box.add_widget(self.card)

        self.add_widget(self.main_box)
