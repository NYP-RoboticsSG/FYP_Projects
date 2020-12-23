from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty

Builder.load_string("""
<ExampleApp>:
    id: main
    orientation: "vertical"
    Button:
        size_hint_x: None
        size_hint_y: None
        height: 30
        width: self.height
        center: self.parent.center
        text: ""
        on_press: gif.anim_delay = 0.09
        on_press: gif._coreimage.anim_reset(True)
        on_press:root.change_state()
        Image:
            id: gif
            source: root.power
            center: self.parent.center
            height: 30
            width: self.height
            allow_stretch: True
            anim_delay: -1
            anim_loop: 1


""")

class ExampleApp(App, BoxLayout):
    power = StringProperty('on_off.gif')

    def build(self):
        return self

    def change_state(self):
        if self.power == 'on_off.gif':
            self.power = 'power on.gif'
        else:
            self.power = 'on_off.gif'

if __name__ == "__main__":
    ExampleApp().run()

# Builder.load_string("""
# <ExampleApp>:
#     orientation: "vertical"
#     Button:
#         text: ""
#         on_press: gif.anim_delay = 0.10
#         on_press: gif._coreimage.anim_reset(True)
#         on_press: root.capture()
#         Image:
#             id: gif
#             source: 'on_off.gif'
#             center: self.parent.center
#             size: 500, 500
#             allow_stretch: True
#             anim_delay: -1
#             anim_loop: 1
# """)
#
# class ExampleApp(App, BoxLayout):
#     def build(self):
#         return self
#
# if __name__ == "__main__":
#     ExampleApp().run()
