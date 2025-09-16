from kivymd.material_resources import dp
from kivymd.uix.recycleboxlayout import MDRecycleBoxLayout
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screen = (
            MDScreen(
                MDRecycleView(
                    MDRecycleBoxLayout(
                        padding=(dp(10), dp(10), 0, dp(10)),
                        default_size=(None, dp(48)),
                        default_size_hint=(1, None),
                        size_hint_y=None,
                        adaptive_height=True,
                        orientation='vertical',
                    ),
                    id="rv",
                ),
                md_bg_color=self.theme_cls.backgroundColor,
            )
        )
        rv = self.screen.get_ids().rv
        rv.key_viewclass = 'viewclass'
        rv.key_size = 'height'
        return self.screen

    def on_start(self):
        for style in theme_font_styles:
            if style != "Icon":
                for role in theme_font_styles[style]:
                    font_size = int(theme_font_styles[style][role]["font-size"])
                    self.screen.get_ids().rv.data.append(
                        {
                            "viewclass": "MDLabel",
                            "text": f"{style} {role} {font_size} sp",
                            "adaptive_height": "True",
                            "font_style": style,
                            "role": role,
                        }
                    )


Example().run()