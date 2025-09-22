import json
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle, Line

from ui.convetor import hex_to_rgba

from kivymd.uix.screen import MDScreen
from kivymd.uix.fitimage import FitImage
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon, MDTextFieldHintText

from kivymd.uix.button import MDButton, MDButtonText

from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout


with open("config.json",'r') as f:
    color_schem = json.load(f)

class Login(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name='login'

        self.startCountWallper = 0
        self.listBackgroundImage = [
            'ui/assets/image/backgroundLogin_1.jpeg',
            'ui/assets/image/backgroundLogin_2.jpg',
            'ui/assets/image/backgroundLogin_3.jpg',
        ]

        self.backgroundImage = FitImage()
        self.add_widget(self.backgroundImage)

        self.boxForm = MDGridLayout(
            cols=1,
            rows=3,
            pos_hint={"x": 0.05, "center_y": 0.6},
            size_hint=(0.25, 0.25),
            padding=[15, 5],
        )

        with self.boxForm.canvas.before:
            Color(*hex_to_rgba(color_schem['playerContentView']))
            self.rect = RoundedRectangle(
                pos=self.boxForm.pos, size=self.boxForm.size, radius=[15]
            )
            Color(*hex_to_rgba(color_schem['playerLine']))  # белая рамка (можешь поменять)
            self.border = Line(rounded_rectangle=[*self.boxForm.pos, *self.boxForm.size, 15], width=2)

        # следим за изменением размеров
        self.boxForm.bind(pos=self._update_rect, size=self._update_rect)

        self.LabelAction = MDLabel(text='Вход',halign='center',font_style='Title', role='large')
        self.boxForm.add_widget(self.LabelAction)


        self.content_box = MDFloatLayout()
        self.iconLead = MDTextFieldLeadingIcon(icon='cellphone-message') 
        self.hintText = MDTextFieldHintText(text='Номер куда надо отпарить код')
        self.phoneInput = MDTextField(
            self.iconLead,
            self.hintText,
            pos_hint={
                'center_x':0.5,
                "center_y":0.5
            }
        )
        self.content_box.add_widget(self.phoneInput)
        self.boxForm.add_widget(self.content_box)

        self.layoutLoginButton = MDFloatLayout()

        self.text = MDButtonText(text='войти') 
        self.btn = MDButton(
            self.text,
            style='filled',
            pos_hint={
                'center_x':0.5,
                "center_y":0.5
            }
        )
        self.layoutLoginButton.add_widget(self.btn)
        self.boxForm.add_widget(self.layoutLoginButton)
        self.add_widget(self.boxForm)

        self.backgroundImage.source = self.listBackgroundImage[self.startCountWallper]
        self.backgroundImage.reload()
        self.startCountWallper += 1
        self.updateWallper = Clock.schedule_interval(self.updateImageBackground, 10)

        self.btn.on_release = self.sendCode

        self.boxLabel = MDBoxLayout(
            pos_hint={"x": 0.53, "y": 0.01},
            orientation="vertical",
            size_hint=(0.45, 0.15),
            padding=[15, 10],
        )

    
        with self.boxLabel.canvas.before:
            # фон
            Color(*hex_to_rgba(color_schem['playerCardTreack']))
            self.bg_rect = RoundedRectangle(
                pos=self.boxLabel.pos,
                size=self.boxLabel.size,
                radius=[15],  # скругления
            )

        # обновление размеров при ресайзе
        self.boxLabel.bind(
            pos=lambda *a: self._update_boxLabel_graphics(),
            size=lambda *a: self._update_boxLabel_graphics()
        )

        self.appName = MDLabel(text='YandeMusic', font_style='Headline', bold=True, role='medium', halign='right')
        self.description = MDLabel(text='Не одобряю пиратство, все что выделаете с клиентом, вы делаете на свой страх и риск!',font_style='Title', role='large', halign='right')
        self.boxLabel.add_widget(self.appName)
        self.boxLabel.add_widget(self.description)
        self.add_widget(self.boxLabel)


    def sendCode(self):
        phone = self.phoneInput.text
        self.phoneInput.text = ''
        print(phone)

        self.text.text= 'Отправить код'
        self.iconLead.icon = 'invoice-send'
        self.hintText.text = 'Введите код из сообщения'

    def updateImageBackground(self, *args):
        anim = Animation(opacity=0, duration=1)  # 1 секунда на исчезновение
        anim.bind(on_complete=self._set_new_background)
        anim.start(self.backgroundImage)

    def _set_new_background(self, *args):
        # подменяем картинку
        self.backgroundImage.source = self.listBackgroundImage[self.startCountWallper]
        self.backgroundImage.reload()
        
        # крутим индекс
        if self.startCountWallper == len(self.listBackgroundImage) - 1:
            self.startCountWallper = 0
        else:
            self.startCountWallper += 1

        # включаем плавное появление
        Animation(opacity=1, duration=1).start(self.backgroundImage)
    

    def _update_rect(self, *args):
        self.rect.pos = self.boxForm.pos
        self.rect.size = self.boxForm.size
        self.border.rounded_rectangle = [*self.boxForm.pos, *self.boxForm.size, 15]

    def _update_boxLabel_graphics(self):
        self.bg_rect.pos = self.boxLabel.pos
        self.bg_rect.size = self.boxLabel.size