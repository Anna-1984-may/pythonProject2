import models
from models import Project, Tag
from utils import saver, current_tags
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from sqlalchemy.ext.declarative import declarative_base
from kivy.uix.screenmanager import SlideTransition, CardTransition, SwapTransition, FadeTransition, WipeTransition, \
    FallOutTransition, RiseInTransition, NoTransition
from kivy.base import runTouchApp
from kivy.storage.jsonstore import JsonStore
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget

# timer_stop_popup = Popup(title='бла-бла',are_u_sure = Label(text='Вы уверены, что хотите остановить таймер?'))

# Window.size = (414,896)

# '[font=OpenSans.ttf]' + 'Войти в аккаунт' + '[/font]', markup = True, font_size = '14sp'

# self.pause_button = Button(text='Пауза', background_color = (0,0,0,0), size_hint=(0.3,3.5), pos_hint={'center_x':0.5,'center_y':-1})

stage = 0
proj_image = '7.png'

user_email = ''
user_login = ''
user_password = ''
flag = 0

Builder.load_string("""
<CurrentTask>:
    canvas.before:
        Color: 
            rgba: (0.26, 0.28, 0.31, 1)
        RoundedRectangle:
            pos:self.pos
            size:self.size
            radius:[10]
""")


class CurrentTask(FloatLayout):
    def __init__(self, my_parent, text, **kwargs):
        self.my_parent = my_parent
        super().__init__(**kwargs)

        self.text = text
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.92}
        self.size_hint = (0.6, 0.1)

        # self.add_widget(Label(text=self.text+'/', font_size='20sp', font_family='OpenSans.ttf'))
        self.add_widget(
            TextInput(size_hint=(0.75, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, text=self.text + ' / ',
                      font_size='20sp', font_family='OpenSans.ttf', cursor_color=(1, 1, 1, 1),
                      on_double_tap=self.do_complete_task, background_color=(0, 0, 0, 0)))
        self.add_widget(Image(source='tick_field.png', pos_hint={'center_x': 0.92, 'center_y': 0.5}))
        self.add_widget(
            Button(size_hint=(0.2, 1), pos_hint={'center_x': 0.92, 'center_y': 0.5}, on_press=self.do_complete_task,
                   background_color=(0, 0, 0, 0)))

    def do_complete_task(self, *args):
        app.sm.get_screen('timer').remove_widget(self)
        app.sm.get_screen('timer').new_sure_finish()


Builder.load_string("""
<NewRoundButton>:
    size_hint: (0.5,0.5)
    canvas.after:
        Color: 
            rgba: (0.58, 0.65, 0.81, 1)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [20]
""")


class NewEnterRoundButton(FloatLayout):
    pass


Builder.load_string("""
<EnterRoundButton>:
    Button:
        background_color: (0,0,0,0)
        size_hint:(0.6,0.2)
        pos_hint:{'center_x':0.5,'center_y':-0.2}
        background_normal:'' 
        text: ''
        text_font: 'OpenSans.ttf'
        on_press: 
        canvas.before:
            Color: 
                rgba: (0.58, 0.65, 0.81, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [16]
""")


class EnterRoundButton(FloatLayout):
    pass


Builder.load_string("""
<ResetRoundButton>:
    Button:
        background_color: (0,0,0,0)
        size_hint:(0.6,0.2)
        pos_hint:{'center_x':0.5,'center_y':-0.2}
        background_normal:'' 
        text: ''
        text_font: 'OpenSans.ttf'
        on_press: 
        canvas.before:
            Color: 
                rgba: (0.33, 0.35, 0.39, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [16]
""")


class ResetRoundButton(FloatLayout):
    pass


Builder.load_string("""
<CreateRoundButton>:
    Button:
        background_color: (0,0,0,0)
        size_hint:(0.6,0.2)
        pos_hint:{'center_x':0.5,'center_y':0.55}
        background_normal:'' 
        text: ''
        text_font: 'OpenSans.ttf'
        canvas.before:
            Color: 
                rgba: (0.33, 0.35, 0.39, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [16]
""")


class CreateRoundButton(FloatLayout):
    pass


Builder.load_string("""
<ForgotPasswordRoundButton>:
    Button:
        background_color: (0,0,0,0)
        size_hint:(0.6,0.2)
        pos_hint:{'center_x':0.5,'center_y':0.55}
        background_normal:'' 
        text: ''
        text_font: 'OpenSans.ttf'
        canvas.before:
            Color: 
                rgba: (0.33, 0.35, 0.39, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [16]
""")


class ForgotPasswordRoundButton(FloatLayout):
    pass


Builder.load_string("""
<ResetAgainButton>:
    Button:
        background_color: (0,0,0,0)
        size_hint:(0.6,0.2)
        pos_hint:{'center_x':0.5,'center_y':0.55}
        background_normal:'' 
        text: ''
        text_font: 'OpenSans.ttf'
        canvas.before:
            Color: 
                rgba: (0.33, 0.35, 0.39, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [16]
""")


class ResetAgainButton(FloatLayout):
    pass


Builder.load_string("""
<ArrowButton>:
    Image:
        source: 'left_arrow.png'
        pos_hint:{'center_x':0.5,'center_y':-0.08}
        size_hint:(100,100)
""")


class ArrowButton(FloatLayout):
    pass


Builder.load_string("""
<LeftArrowButton>:
    Image:
        source: 'Left arrow.png'
        pos_hint:{'center_x':0.08,'center_y':0.95}
""")


class LeftArrowButton(FloatLayout):
    pass


Builder.load_string("""
<RightArrowButton>:
    Image:
        source: 'Right arrow.png'
        pos_hint:{'center_x':0.92,'center_y':0.95}
""")


class RightArrowButton(FloatLayout):
    pass


Builder.load_string("""
<TestBottomBar>:
    BoxLayout:
        MDBottomAppBar:
            MDToolbar:
                title: '_test_'
                mode: 'end'
                type: 'bottom'

""")


class TestBottomBar(FloatLayout):
    pass


Builder.load_string("""
<Base>:
    Image:
        source: 'round_timer.png'    
        pos_hint:{'center_y':4.95,'center_x':0.5}  
        size_hint:(105,105) 
        border: 1,1,1,1
        text:'*круг таймера'
""")


class Base(FloatLayout):
    pass


Builder.load_string("""
<RoundButton>
    Button:
        background_normal: 'enter_account.png'
        border: 1,1,1,1
        text: '[font=OpenSans.ttf]' + 'Войти в аккаунт' + '[/font]'
        markup:True
        font_size: '20sp'
        size_hint:(0.5,0.9)
        pos_hint:{'center_x':0.5,'center_y':0.8}
        on_press: self.next_signin
""")


class RoundButton(FloatLayout):
    pass


Builder.load_string("""
<Avatar>:
    Image:
        source:'ava.png'
        size_hint:(1000,1000)
        pos_hint:{'center_x':0.5,'center_y':0.5}
""")


class Avatar(FloatLayout):
    pass


Builder.load_string("""
<InputBackground>:
    Button:
        background_color: (0,0,0,0)
        size_hint:(0.9,0.3)
        pos_hint:{'center_x':0.5,'center_y':0.5}
        background_normal:'' 
        text: ''
        text_font: 'OpenSans.ttf'
        canvas.before:
            Color: 
                rgba: (0.26,0.28,0.31,1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [10]
""")


class InputBackground(FloatLayout):
    pass


Builder.load_string("""
<StatusBackground>:
    Button:
        background_color: (0,0,0,0)
        size_hint:(1,0.7)
        pos_hint:{'center_x':0.5,'center_y':0.5}
        background_normal:'' 
        text: ''
        text_font: 'OpenSans.ttf'
        on_press: print('1')
        canvas.before:
            Color: 
                rgba: (0.26,0.28,0.31,1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [8]
""")


class StatusBackground(FloatLayout):
    pass


Builder.load_string("""
<SelectStatusBackground>:
    Button:
        background_color: (0,0,0,0)
        size_hint:(0.33,0.7)
        pos_hint:{'center_x':0.5,'center_y':0.5}
        background_normal:'' 
        text: ''
        text_font: 'OpenSans.ttf'
        on_press: print('1')
        canvas.before:
            Color: 
                rgba: (0.58, 0.65, 0.81, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [8]
""")


class SelectStatusBackground(FloatLayout):
    pass


Builder.load_string("""
<SelectImButton>:
    GridLayout:
        cols:5
        size_hint:(0.9,0.3)
        pos_hint:{'center_x':0.5,'center_y':0.18}
        canvas.before:
            Color:
                rgba: (0.26,0.28,0.31,1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [20]
""")


class SelectImButton(FloatLayout):
    pass


Builder.load_string("""
<TagListBackground>:
    BoxLayout:
        size_hint:(0.9,0.2)
        pos_hint:{'center_x':0.5,'center_y':0.58}
        canvas.before:
            Color:
                rgba: (0.26,0.28,0.31,1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [15]
""")


class TagListBackground(FloatLayout):
    pass


# self.add_tag_input.text

Builder.load_string("""
<TagBackground>:
    FloatLayout:
        size: root.size
        pos: root.pos    
        canvas.before:
            Color:
                rgba: (0.58, 0.65, 0.81, 1)
            RoundedRectangle:
                size: root.size
                pos: root.pos
                radius: [20]
    Label:
        pos: root.pos
        size: root.size
        text: root.text
""")
'''
class TagBackground_back(FloatLayout):
    def __init__(self, pos, size, **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.size = size
'''
tagss = []


class TagBackground(Button):
    def __init__(self, screen, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        # screen.manager.get_screen('createproject').ids.tag_list.tags.append(text)
        tag = text
        tagss.append(text)
        self.background_color = (0, 0, 0, 0)
        # app.sm.get_screen('createproject').ids.tag_list.add_widget(TagBackground_back(pos=self.pos, size=self.size))
        # self.pos = app.sm.get_screen('createproject').ids.tag_list.pos
        # self.add_widget(TagBackground_back(pos=self.pos,size=self.size))

    def on_press(self):
        app.sm.get_screen('createproject').ids.tag_list.remove_widget(self)
        current_tags.remove(self.text)


Builder.load_string("""
<SearchButtonBackground>:
    Button:
        background_color: (0,0,0,0)
        size_hint: (0.9,0.4)
        pos_hint: {'center_x':0.5,'center_y':4.5}
        canvas.before:
            Color:
                rgba: (0.58, 0.65, 0.81, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [10]
    Button:
        background_color: (0,0,0,0)
        size_hint: (0.89,0.36)
        pos_hint: {'center_x':0.5,'center_y':4.5}
        canvas.before:
            Color:
                rgba: (0.26,0.28,0.31,1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [10]
    Image:
        source: 'Search_small.png'
        pos_hint: {'center_x':0.14,'center_y':4.5}

""")


class SearchButtonBackground(FloatLayout):
    pass


Builder.load_string("""
<BottomPanelBackground>:
    FloatLayout:
        orientation: 'vertical'
        Button:
            pos_hint: {'center_x':0.5,'center_y':0.5}
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0]
        Button:
            pos_hint: {'center_x':0.5,'center_y':0.9}
            size_hint: (0.4,0.8)
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [10000]
        Image:
            source: 'Timer.png'
            pos_hint: {'center_y':0.5,'center_x':0.1}
        Image:
            source: 'Statistics.png'
            pos_hint: {'center_y':0.5,'center_x':0.25}
        Image:
            source: 'Plus.png'
            pos_hint: {'center_y':0.6,'center_x':0.5}
        Image:
            source: 'Profile.png'
            pos_hint: {'center_y':0.5,'center_x':0.75}
        Image:
            source: 'Settings.png'
            pos_hint: {'center_y':0.5,'center_x':0.9}


""")


class BottomPanelBackground(FloatLayout):
    pass


Builder.load_string("""
<BottomPanelBackground_timer>:
    FloatLayout:
        orientation: 'vertical'
        Button:
            pos_hint: {'center_x':0.5,'center_y':0.5}
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0]
        Button:
            pos_hint: {'center_x':0.5,'center_y':0.9}
            size_hint: (0.4,0.8)
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [10000]
        Image:
            source: 'Timer_bold.png'
            pos_hint: {'center_y':0.5,'center_x':0.1}
        Image:
            source: 'Statistics.png'
            pos_hint: {'center_y':0.5,'center_x':0.25}
        Image:
            source: 'Home.png'
            pos_hint: {'center_y':0.6,'center_x':0.5}
        Image:
            source: 'Profile.png'
            pos_hint: {'center_y':0.5,'center_x':0.75}
        Image:
            source: 'Settings.png'
            pos_hint: {'center_y':0.5,'center_x':0.9}


""")


class BottomPanelBackground_timer(FloatLayout):
    pass


Builder.load_string("""
<BottomPanelBackground_stats>:
    FloatLayout:
        orientation: 'vertical'
        Button:
            pos_hint: {'center_x':0.5,'center_y':0.5}
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0]
        Button:
            pos_hint: {'center_x':0.5,'center_y':0.9}
            size_hint: (0.4,0.8)
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [10000]
        Image:
            source: 'Timer.png'
            pos_hint: {'center_y':0.5,'center_x':0.1}
        Image:
            source: 'Statistics_bold.png'
            pos_hint: {'center_y':0.5,'center_x':0.25}
        Image:
            source: 'Home.png'
            pos_hint: {'center_y':0.6,'center_x':0.5}
        Image:
            source: 'Profile.png'
            pos_hint: {'center_y':0.5,'center_x':0.75}
        Image:
            source: 'Settings.png'
            pos_hint: {'center_y':0.5,'center_x':0.9}


""")


class BottomPanelBackground_stats(FloatLayout):
    pass


Builder.load_string("""
<BottomPanelBackground_profile>:
    FloatLayout:
        orientation: 'vertical'
        Button:
            pos_hint: {'center_x':0.5,'center_y':0.5}
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0]
        Button:
            pos_hint: {'center_x':0.5,'center_y':0.9}
            size_hint: (0.4,0.8)
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [10000]
        Image:
            source: 'Timer.png'
            pos_hint: {'center_y':0.5,'center_x':0.1}
        Image:
            source: 'Statistics.png'
            pos_hint: {'center_y':0.5,'center_x':0.25}
        Image:
            source: 'Home.png'
            pos_hint: {'center_y':0.6,'center_x':0.5}
        Image:
            source: 'Profile_bold.png'
            pos_hint: {'center_y':0.5,'center_x':0.75}
        Image:
            source: 'Settings.png'
            pos_hint: {'center_y':0.5,'center_x':0.9}


""")


class BottomPanelBackground_profile(FloatLayout):
    pass


Builder.load_string("""
<BottomPanelBackground_settings>:
    FloatLayout:
        orientation: 'vertical'
        Button:
            pos_hint: {'center_x':0.5,'center_y':0.5}
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0]
        Button:
            pos_hint: {'center_x':0.5,'center_y':0.9}
            size_hint: (0.4,0.8)
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [10000]
        Image:
            source: 'Timer.png'
            pos_hint: {'center_y':0.5,'center_x':0.1}
        Image:
            source: 'Statistics.png'
            pos_hint: {'center_y':0.5,'center_x':0.25}
        Image:
            source: 'Home.png'
            pos_hint: {'center_y':0.6,'center_x':0.5}
        Image:
            source: 'Profile.png'
            pos_hint: {'center_y':0.5,'center_x':0.75}
        Image:
            source: 'Settings_bold.png'
            pos_hint: {'center_y':0.5,'center_x':0.9}


""")


class BottomPanelBackground_settings(FloatLayout):
    pass


Builder.load_string("""
<ProjectIconBackground>:
    BoxLayout:
        padding: 10
        orientation: 'horizontal'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        Button:
            pos_hint:{'center_y':0.5}
            size_hint: (0.8,2)
            background_color: (0,0,0,0)
            canvas.before:
                Color:
                    rgba: (0.58, 0.65, 0.81, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [20]


""")


class ProjectIconBackground(FloatLayout):
    pass


project_number = []

Builder.load_string("""
#: import Window kivy.core.window.Window
<Main>:
    BoxLayout:
        orientation:'vertical'
        pos_hint:{'center_y':0.55}
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            project_number: []
            GridLayout:
                id: main_grid
                cols:2
                orientation: 'lr-tb'
                size_hint_y:None
                height: Window.height * 2
                spacing: 10
                padding: 20

                GridLayout:
                    cols: 1
                    orientation: 'lr-tb'
                    id: left_box
                    orientatin: 'vertical'
                    padding: 10
                    spacing: 20
                    Button:
                        size_hint:(0.9, None)
                        background_color: (0,0,0,0)


                GridLayout:
                    cols: 1
                    orientation: 'rl-tb'
                    id: right_box
                    orientatin: 'vertical'
                    padding: 10
                    spacing: 20
                    Button:
                        size_hint:(0.9, None)
                        background_color: (0,0,0,0)


    FloatLayout:
        size_hint:(1,0.2)
        pos_hint:{'center_x':0.5,'center_y':0.5}

        SearchButtonBackground

        BoxLayout:
            id: seacrh_layout
            orientation:'horizontal'
            size_hint:(0.85,0.4)
            pos_hint:{'center_x':0.5,'center_y':2.45}
            Button:
                text:''
                size_hint:(0.15,1)
                background_color:(0,0,0,0)
                on_press: root.do_searching(query=search_text.text)
            TextInput:
                id: search_text
                hint_text:'Поиск'
                hint_text_color:(0.36,0.39,0.43,1)
                font_size:'20sp'
                halign:'left'
                focus:False
                multiline:False
                background_color:(0,0,0,0)

    BoxLayout:
        orientation:'horizontal'
        size_hint:(1,0.125)
        pos_hint:{'center_x':0.5}

        BottomPanelBackground

""")

'''
                    Button:
                        text: '<test>'
                        size_hint:(0.9, None)
                        size_y: 50
'''

Builder.load_string("""
<CreateProject>:
    id: create_proj
    BoxLayout:
        orientation:'vertical'
        spacing:4
        padding:8
        pos_hint:{'center_x':0.5,'center_y':0.9}
        BoxLayout:
            orientation:'horizontal'
            spacing: 30
            Label:
                text: 'Отменить'
                text_font: 'OpenSans.ttf'
                markup:True
                font_size:'14sp'
            Label:
                text:'Новый проект'
                text_font: 'OpenSans.ttf'
                markup:True
                font_size:'20sp'
            Label:
                text:'Создать'
                text_font: 'OpenSans.ttf'
                markup:True
                font_size:'14sp'

    BoxLayout:
        orientation:'vertical'
        pos_hint:{'center_y':0.58}
        BoxLayout:
            orientation:'horizontal'
            Button:
                background_color: (0,0,0,0)
                size_hint:(0.7,0.4)
                pos_hint:{'center_x':0.5,'center_y':0.5}
                on_press: root.cancel()
            Label:
                text:''
            Button:
                background_color:(0,0,0,0)
                size_hint:(0.7,0.4)
                pos_hint:{'center_x':0.5,'center_y':0.5}
                on_press: root.create(proj_name.text, select_status.status)
        Label:
            text: ''
        Label:
            text: ''
    TagListBackground

    FloatLayout:
        size_hint:(1,0.2)
        pos_hint:{'center_x':0.5,'center_y':0.8}
        InputBackground:
            pos_hint:{'center_x':0.5, 'center_y':0.5}
        TextInput:
            id: proj_name
            hint_text:'Название'
            hint_text_color:(0.36,0.39,0.43,1)
            background_color:(0,0,0,0)
            font_size:'14sp'
            halign:'left'
            focus:False
            multiline:False
            size_hint:(0.88,0.4)
            pos_hint:{'center_x':0.5, 'center_y':0.43}
        InputBackground:
            pos_hint:{'center_x':0.5,'center_y':-1.5}
        BoxLayout:
            id: selected_status_layout_background
            orientation:'horizontal'
            size_hint:(0.9,0.4)
            pos_hint:{'center_x':0.2,'center_y':-1.5}
            SelectStatusBackground
        BoxLayout:
            id: select_status
            orientation:'horizontal'
            size_hint:(0.9,0.4)
            pos_hint:{'center_x':0.5,'center_y':-1.5}
            status: (0.58,0.65,0.81,1)
            ToggleButton:
                id: status_norm
                text: 'Обычный'
                text_font: 'OpenSans.ttf'
                markup:True
                font_size:'14sp'
                group:'status'
                state:'down'
                background_color: (0,0,0,0)
                on_press: root.change_status_norm()
            ToggleButton:
                id: status_long
                text: 'Затяжной'
                text_font: 'OpenSans.ttf'
                markup:True
                font_size:'14sp'
                group:'status'
                background_color: (0,0,0,0)
                on_press: root.change_status_long()
            ToggleButton:
                id: status_short
                text:'Срочный'
                text_font: 'OpenSans.ttf'
                markup:True
                font_size:'14sp'
                group:'status'
                background_color: (0,0,0,0)
                on_press: root.change_status_short()
        BoxLayout:
            orientation:'vertical'
            pos_hint:{'center_y':0.1}
            InputBackground
        BoxLayout:
            orientation:'horizontal'
            size_hint:(0.9,0.4)
            pos_hint:{'center_x':0.8, 'center_y':0.1}
            SelectStatusBackground
        BoxLayout:
            orientation:'horizontal'
            size_hint:(0.88,0.4)
            pos_hint:{'center_x':0.5, 'center_y':0.1}
            FloatLayout:
                size_hint:(0.66,1)
                TextInput:
                    id: add_tag_input
                    hint_text:'Ведите тег'
                    hint_text_color:(0.36,0.39,0.43,1)
                    background_color:(0,0,0,0)
                    font_size:'14sp'
                    halign:'left'
                    focus:False
                    multiline:False
                    pos_hint:{'center_x':0.5, 'center_y':0.32}
                    on_focus:
                        root.delete_input_text()
            Button:
                id: add_tag_button
                background_color:(0,0,0,0)
                size_hint:(0.33,1)
                text:'  Добавить'
                text_font: 'OpenSans.ttf'
                markup:True
                font_size:'14sp'
                on_press: root.add_tag()
        GridLayout:
            id: tag_list
            proj_num_for_screen_height:[]
            proj_num_for_screen_height_i: 1
            spacing:10
            padding:5
            cols:5
            size_hint:(0.9,0.9)
            pos_hint:{'center_x':0.5,'center_y':-0.6}
    BoxLayout:
        orientation:'vertical'
        pos_hint:{'center_x':0.6,'center_y':0.45}
        Label:
            text:'Статус'
            text_font: 'OpenSans.ttf'
            markup:True
            font_size:'14sp'
            pos_hint:{'center_x':0.1}
            color:(0.36,0.39,0.43,1)
    BoxLayout:
        orientation:'vertical'
        pos_hint:{'center_x':0.57,'center_y':0.35}
        Label:
            text: 'Изображение'
            text_font: 'OpenSans.ttf'
            markup:True
            font_size:'14sp'
            pos_hint:{'center_x':0.2}
            color:(0.36,0.39,0.43,1)
    BoxLayout:
        orientation:'vertical'
        SelectImButton
    GridLayout:
        cols:5
        size_hint:(0.9,0.3)
        pos_hint:{'center_x':0.5,'center_y':0.18}
        ToggleButton:
            group:'select_image'
            text:'1'
            background_color:(0,0,0,0)
            on_press: root.tick_image_1()
        ToggleButton:
            group:'select_image'
            text:'2'
            background_color:(0,0,0,0)
            on_press: root.tick_image_2()
        ToggleButton:
            group:'select_image'
            text:'3'
            background_color:(0,0,0,0)
            on_press: root.tick_image_3()
        ToggleButton:
            group:'select_image'
            text:'4'
            background_color:(0,0,0,0)
            on_press: root.tick_image_4()
        ToggleButton:
            group:'select_image'
            text:'5'
            background_color:(0,0,0,0)
            on_press: root.tick_image_5()
        ToggleButton:
            group:'select_image'
            text:'6'
            background_color:(0,0,0,0)
            on_press: root.tick_image_6()
        ToggleButton:
            group:'select_image'
            text:'7'
            background_color:(0,0,0,0)
            on_press: root.tick_image_7()
        ToggleButton:
            group:'select_image'
            text:'8'
            background_color:(0,0,0,0)
            on_press: root.tick_image_8()
        ToggleButton:
            group:'select_image'
            text:'9'
            background_color:(0,0,0,0)
            on_press: root.tick_image_9()
        ToggleButton:
            group:'select_image'
            text:'10'
            background_color:(0,0,0,0)
            on_press: root.tick_image_10()
        ToggleButton:
            group:'select_image'
            text:'11'
            background_color:(0,0,0,0)
            on_press: root.tick_image_11()
        ToggleButton:
            group:'select_image'
            text:'12'
            background_color:(0,0,0,0)
            on_press: root.tick_image_12()
        ToggleButton:
            group:'select_image'
            text:'13'
            background_color:(0,0,0,0)
            on_press: root.tick_image_13()
        ToggleButton:
            group:'select_image'
            text:'14'
            background_color:(0,0,0,0)
            on_press: root.tick_image_14()
        ToggleButton:
            group:'select_image'
            text:'15'
            background_color:(0,0,0,0)
            on_press: root.tick_image_15()
    GridLayout:
        cols:5
        size_hint:(0.9,0.3)
        pos_hint:{'center_x':0.5,'center_y':0.18}
        spacing:5
        padding:10
        Image:
            id: Img1
            source:'1.png'
        Image:
            id: Img2
            source:'2.png'
        Image:
            id: Img3
            source:'3.png'
        Image:
            id: Img4
            source:'4.png'
        Image:
            id: Img5
            source:'5.png'
        Image:
            id: Img6
            source:'6.png'
        Image:
            id: Img7
            source:'7.png'
        Image:
            id: Img8
            source:'8.png'
        Image:
            id: Img9
            source:'9.png'
        Image
            id: Img10
            source:'10.png'
        Image:
            id: Img11
            source:'11.png'
        Image:
            id: Img12
            source:'12.png'
        Image:
            id: Img13
            source:'13.png'
        Image:
            id: Img14
            source:'14.png'
        Image:
            id: Img15
            source:'15.png'

""")

Builder.load_string("""
<ProjectScreenBackground>:
    canvas.before:
        Color:
            rgba: (0.58, 0.65, 0.81, 1)
        Rectangle:
            pos: self.pos
            size: self.size
""")


class ProjectScreenBackground(FloatLayout):
    pass


Builder.load_string("""
<PopUpWidget>:
    Button:
        background_color: (0,0,0,0)
        size_hint: (0.55,0.025)
        pos_hint:{'center_x':0.5,'center_y':0.02}
        canvas.before:
            Color:
                rgba: (0.26, 0.28, 0.31, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [8]

""")


class PopUpWidget(FloatLayout):
    pass


Builder.load_string("""
<PopDownWidget>:
    Button:
        background_color: (0,0,0,0)
        size_hint: (2,0.25)
        pos_hint:{'center_x':0.5,'center_y':0.5}
        canvas.before:
            Color:
                rgba: (0.15, 0.18, 0.20, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [5]
""")


class PopDownWidget(FloatLayout):
    pass


Builder.load_string("""
<BottomPanel>:
    Button:
        id: panel
        background_color: (0,0,0,0)
        size_hint: (0.85, 0.12)
        pos_hint:{'center_x':0.5,'center_y':0.065}
        canvas.before:
            Color:
                rgba: (0.26, 0.28, 0.31, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [8]
        BoxLayout:
            orientation: 'horizontal'
            size: panel.size
            pos: panel.pos
            Image:
                source: 'home_round.png'
            Widget:
            BoxLayout:
                orientation: 'vertical'
                pos_hint:{'center_y':0.58}
                PopDownWidget
                BoxLayout:
                    size_hint: (2.8,1)
                    pos_hint: {'center_x':0.5}
                    orientation: 'horizontal'
                    spacing: 5
                    Image:
                        source: 'picture_box.png'
                    Image:
                        source: 'uzel_box.png'
                    Image:
                        source: 'uzel_2_box.png'
                    Image:
                        source: 'bin_box.png'
            Widget:
            Image:
                source: 'timer_rounded.png'
""")


class BottomPanel(FloatLayout):
    pass


#        my_color: root.ids.status
# (0.58,0.65,0.81,1)(0.85,0.67,0.21,1)(0.76,0.11,0.11,1)


Builder.load_string("""
<ProjectButton>:
    Widget:
        pos: root.pos
        size: root.size
        my_status_color: (0.58,0.65,0.81,1)
        canvas.before: 
            Color: 
                rgba: self.my_status_color
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [10]
        Label:
            pos: root.pos
            size: root.size
            text: root.text


""")

Builder.load_string("""
<TaskBackground>:
    Button:
        id: main_button
        size: root.size
        pos: root.pos
        background_color: (0,0,0,0)
        Widget
            id: color_change
            size: root.size
            pos: root.pos
            my_color: (1,1,1,1)
            canvas.before:
                Color: 
                    rgba: self.my_color
                RoundedRectangle:
                    pos:self.pos
                    size:self.size
                    radius:[20]
        BoxLayout:
            pos: root.pos
            width: root.width * 1.5
            orientation: 'horizontal'
            TextInput:
                halign: 'center'
                pos:root.pos
                size:root.size
                background_color: (0,0,0,0)
                on_triple_tap: root.delete_task()
                on_double_tap: root.ids.color_change.my_color = (0.31,0.81,0.36,1)
                font_name: 'OpenSans.ttf'
                on_focus: 
            Button:
                id:plus_button
                size_hint:(0.5,0.5)
                pos_hint:{'center_x':0,'center_y':0.5}
                background_color: (0,0,0,0)
                on_press: root.add_new_task()
                Image:
                    source: 'rounded_plus.png'
                    pos:plus_button.pos
                    size:plus_button.size

""")
'''
'''

tasks_number = []
index_number = 1
current_grid = None


class ListWithTasks(list):
    def __init__(self, my_parent, num, **kwargs):
        self.my_parent = my_parent
        super().__init__(**kwargs)
        self.num = num
        i = 0
        for i in range(self.num):
            self.append(i)
            i += 1


class TaskBackground(Button):
    def __init__(self, my_parent, **kwargs):
        self.my_parent = my_parent
        super().__init__(**kwargs)

        self.name = my_parent

        self.background_color = (0, 0, 0, 0)
        self.size_hint = (None, None)
        self.size_x = 500
        self.size_y = 50

    def add_new_task(self, **args):
        app.sm.get_screen(self.my_parent).main_grid.add_widget(TaskBackground(my_parent=self.name))

    # app.sm.get_screen(self.my_parent).add_widget(TaskBackground(my_parent = self.name, pos_hint={'center_x':0.5,'center_y':0.5}))

    def delete_task(self, **args):
        app.sm.get_screen(self.my_parent).main_grid.remove_widget(self)


class TasksGrid(GridLayout):
    def __init__(self, my_parent, **kwargs):
        self.my_parent = my_parent
        super().__init__(**kwargs)

        self.name = my_parent
        self.size_hint = (None, None)
        self.cols = 1
        self.rows = 1

        self.add_widget(TaskBackground(my_parent=self.name))

    def add_new_parallel_task(self, **args):
        # app.sm.get_screen(self.my_parent).main_grid.
        self.spacing = 10
        self.rows += 1
        self.add_widget(TaskBackground(my_parent=self.name))
        # (GridLayout(rows=1, padding=(40,200,1,1), spacing=10, row_force_default=False, orientation='lr-tb', size_hint=(None,None), width = Window.width * 20))
        # (TaskBackground(my_parent = self.name))


# python app.py -m screen:phone_iphone_5,portrait,scale.75

dark_background_color = (0.15, 0.18, 0.20, 1)
button_color = (0.58, 0.65, 0.81, 1)
light_grey = (0.26, 0.28, 0.31, 1)

status_color_norm = (0.58, 0.65, 0.81, 1)
status_color_short = (0.76, 0.11, 0.11, 1)
status_color_long = (0.85, 0.67, 0.21, 1)

txt_exit = '[color=#FF0404]' + 'Выйти из аккаунта' + '[/color]'
# text='[font=OpenSans.ttf]' + '' + '[/font]', markup=True, font_size='sp'


Window.clearcolor = dark_background_color

project_number_i = 1


class New_Project(Button):
    def __init__(self, screen, goal, name, **kwargs):
        super().__init__(**kwargs)
        self.goal = goal
        self.screen = screen
        self.name = name
        # self.status = status
        # self.describtion = describtion

        # self.text = self.manager.get_screen('createproject').ids.proj_name.text
        # self.background_normal = proj_image

    def on_press(self):
        self.screen.manager.current = self.goal


class ProjectButton(Button):
    def __init__(self, screen, goal, name, my_parent, status, project_tags, tag, **kwargs):
        self.my_parent = my_parent
        super().__init__(**kwargs)
        self.screen = screen
        self.goal = name
        global flag
        if flag == 1:
            self.status = (0.58, 0.65, 0.81, 1)
        elif flag == 2:
            self.status = (0.76, 0.11, 0.11, 1)
        elif flag == 3:
            self.status = (0.85, 0.67, 0.21, 1)

        #self.status = status
        status_color = (1, 1, 1, 1)

        """
        if self.status == [0.58, 0.65, 0.81, 1]:
            # self.ids.my_status_color = (0.58,0.65,0.81,1)
            self.change_color_blue()
        elif self.status == [0.76, 0.11, 0.11, 1]:
            # self.ids.my_status_color = (0.76,0.11,0.11,1)
            self.change_color_red()
        elif self.status == [0.85, 0.67, 0.21, 1]:
            # self.ids.my_status_color = (0.85,0.67,0.21,1)
            self.change_color_yellow()
"""
        self.background_color = (0, 0, 0, 0)

        self.size_hint = (0.9, None)
        self.size_y = 50
       # self.project_tags = tagss
        self.text = name
        self.tag = tag

        if saver(name, tag):
            pass
    def on_press(self, **args):
        # self.my_parent.change_color(self)
        self.screen.manager.current = self.goal

    def change_color_blue(self, **args):
        self.ids.my_status_color = (0.58, 0.65, 0.81, 1)

    def change_color_red(self, **args):
        self.ids.my_status_color = (0.76, 0.11, 0.11, 1)

    def change_color_yellow(self, **args):
        self.ids.my_status_color = (0.85, 0.67, 0.21, 1)

"""
        i = 0

        tags = []
        for i in range(len(tagss)):
            tags.append(project_tags[i])
            i += 1

        print(tags)
"""







class ProjectButtonScreen(Screen):
    def __init__(self, name, my_parent, **kwargs):
        self.my_parent = my_parent
        self.name = name
        super().__init__(**kwargs)

        backgroundcolor = ProjectScreenBackground()
        self.add_widget(backgroundcolor)

        #################################################################################################################
        # , rows_minimum={0:???}   col_default_width=???,
        self.scroll = ScrollView(do_scroll_y=True, do_scroll_x=True, size_hint=(1, 1))

        # self.vertical_main_grid = GridLayout(rows=7, padding=(40,200,1,1), spacing=10, row_force_default=False, orientation='lr-tb', size_hint=(None,None), width = Window.width * 20, height = Window.height * 20)

        self.main_grid = GridLayout(rows=1, padding=(40, 200, 1, 1), spacing=10, row_force_default=False,
                                    orientation='lr-tb', size_hint=(None, None), width=Window.width * 20,
                                    height=Window.height * 20)
        # self.current_grid = self.main_grid
        # current_grid = self.main_grid
        self.starter_task = TasksGrid(my_parent=self.name)
        self.main_grid.add_widget(self.starter_task)

        # self.second_grid = GridLayout(rows=1, padding=(40,200,1,1), spacing=10, row_force_default=False, orientation='lr-tb', size_hint=(None,None), width = Window.width * 20, height = Window.height * 20)
        # self.third_grid = GridLayout(rows=1, padding=(40,200,1,1), spacing=10, row_force_default=False, orientation='lr-tb', size_hint=(None,None), width = Window.width * 20, height = Window.height * 20)
        # elf.vertical_main_grid.add_widget(self.main_grid)
        # self.vertical_main_grid.add_widget(self.second_grid)
        # self.vertical_main_grid.add_widget(self.third_grid)

        # self.scroll.add_widget(self.vertical_main_grid)

        self.scroll.add_widget(self.main_grid)
        self.add_widget(self.scroll)
        #################################################################################################################

        self.firstwidget = PopUpWidget()
        self.bottom_panel = BottomPanel()

        self.layout_v_main = FloatLayout(orientation='vertical')

        self.popup_button = Button(size_hint=(0.6, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0},
                                   background_color=(0, 0, 0, 0))
        self.popup_button.on_press = self.show_widget

        self.upper_layout = FloatLayout()
        left_arrow_img = LeftArrowButton()
        right_arrow_img = RightArrowButton()
        upper_layout_h = BoxLayout(orientation='horizontal', pos_hint={'center_x': 0.5, 'center_y': 0.95})
        left_arrow_button = Button(size_hint=(0.4, 0.1), pos_hint={'center_y': 0.5}, background_color=(0, 0, 0, 0))
        right_arrow_button = Button(size_hint=(0.4, 0.1), pos_hint={'center_y': 0.5}, background_color=(0, 0, 0, 0))
        project_name = Label(text=name, font_family='OpenSans.ttf', font_size='20sp')
        upper_layout_h.add_widget(left_arrow_button)
        upper_layout_h.add_widget(project_name)
        upper_layout_h.add_widget(right_arrow_button)
        self.upper_layout.add_widget(left_arrow_img)
        self.upper_layout.add_widget(upper_layout_h)
        self.upper_layout.add_widget(right_arrow_img)

        self.layout_bottom_panel_h = BoxLayout(orientation='horizontal', size_hint=(0.85, 0.15),
                                               pos_hint={'center_x': 0.5})
        home = ScrButton(self, text='', goal='main', background_color=(0, 0, 0, 0), size_hint=(0.4, 1))
        home.bind(on_press=self.clearing_list)
        gotimer = ScrButton(self, text='', goal='timer', background_color=(0, 0, 0, 0), size_hint=(0.4, 1))
        gotimer.bind(on_press=self.go_timer)
        addit_bottom_panel_layout_v = BoxLayout(orientation='vertical')
        popdown_button = Button(background_color=(0, 0, 0, 0), size_hint=(1, 0.8))
        popdown_button.on_press = self.hide_widget
        addit_bottom_panel_layout_h = BoxLayout(orientation='horizontal')
        button_image = Button(background_color=(0, 0, 0, 0))
        button_pack_1 = Button(background_color=(0, 0, 0, 0))
        button_pack_1.on_press = self.add_new_parallel_task
        button_pack_2 = Button(background_color=(0, 0, 0, 0))
        button_bin = ScrButton(self, goal='main', background_color=(0, 0, 0, 0))
        button_bin.on_press = self.delete_project
        addit_bottom_panel_layout_h.add_widget(button_image)
        addit_bottom_panel_layout_h.add_widget(button_pack_1)
        addit_bottom_panel_layout_h.add_widget(button_pack_2)
        addit_bottom_panel_layout_h.add_widget(button_bin)
        addit_bottom_panel_layout_v.add_widget(popdown_button)
        addit_bottom_panel_layout_v.add_widget(addit_bottom_panel_layout_h)
        self.layout_bottom_panel_h.add_widget(home)
        self.layout_bottom_panel_h.add_widget(addit_bottom_panel_layout_v)
        self.layout_bottom_panel_h.add_widget(gotimer)

        self.layout_v_main.add_widget(self.firstwidget)
        self.layout_v_main.add_widget(self.popup_button)

        self.add_widget(self.layout_v_main)

        ##########################################################################################################################################
        ##########################################################################################################################################
        # sm = ScreenManager()
        # self.current_screen = ProjectButtonScreen(name=name)
        # self.sm.add_widget(self.current_screen)
        # test_inp = TextInput(halign='left', focus=False, multiline=False, background_color=(0,0,0,1), size_hint=(0.85,0.2))
        # test_inp = TaskBackground(my_parent = self.name, color='red')
        # self.add_widget(test_inp)

    def go_timer(self, *args):
        app.sm.get_screen('timer').add_widget(CurrentTask(my_parent=self.name, text=self.name))

    def add_new_parallel_task(self, **args):
        self.starter_task.add_new_parallel_task()

    def hide_widget(self, **args):
        self.layout_v_main.remove_widget(self.layout_bottom_panel_h)
        self.layout_v_main.remove_widget(self.bottom_panel)
        self.layout_v_main.add_widget(self.popup_button)
        self.layout_v_main.remove_widget(self.upper_layout)

    def show_widget(self, **args):
        self.layout_v_main.add_widget(self.bottom_panel)
        self.layout_v_main.add_widget(self.layout_bottom_panel_h)
        self.layout_v_main.remove_widget(self.popup_button)
        self.layout_v_main.add_widget(self.upper_layout)

    def delete_project(self, **args):
        # self.screen.manager.current = 'main'
        app.sm.get_screen('main').ids.left_box.remove_widget(self.name)

    def clearing_list(self, *args, **kwargs):
        global index_number
        index_number = 1


class Seconds(Button):
    done = BooleanProperty(False)

    def __init__(self, total, background_color, size_hint, pos_hint, font_size, font_name, **kwargs):
        self.total = total
        self.current = total
        self.background_color = background_color
        self.size_hint = size_hint
        self.pos_hint = pos_hint
        self.font_size = font_size
        self.font_name = font_name
        self.done = False
        text_1 = str(self.current // 60) + ":" + str(self.current % 60 * (1)) + '0'
        super().__init__(text=text_1)

    def restart(self, total, **kwargs):
        self.done = False
        self.total = total
        self.current = total
        text_1 = str(self.current // 60) + ":" + str(self.current % 60 * (1)) + '0'
        self.text = str(self.current // 60) + ":" + str(self.current % 60 * (1)) + '0'
        self.stop()
        global stage
        stage = 0

    def start(self):
        Clock.schedule_interval(self.change, 1)

    def stop(self):
        Clock.unschedule(self.change)

    def change(self, dt):
        self.current -= 1
        self.text = str(self.current // 60) + ":" + str(self.current % 60 * (1))
        # self.text = str(self.current)
        if self.current == 0:
            self.stop()
            self.done = True
            return False


class Llabel(Label):
    def __init__(self, text, goal, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.goal = goal


'''
    def on_press(self):
        self.screen.manager.current = self.goal
'''


class ScrButton(Button):
    def __init__(self, screen, direction='right', goal='first', **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.direction = direction
        self.goal = goal

    def on_press(self):
        self.screen.manager.transition.direction = self.direction
        self.screen.manager.current = self.goal

    def nulstage(self):
        global stage
        stage = 0


def check_int(str_num):
    try:
        return int(str_num)
    except:
        return False


class NextScreenButton(Button):
    def __init__(self, screen, goal='main', **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.goal = goal

    def on_press(self):
        self.screen.manager.current = self.goal


class FirstScreen(Screen):
    def __init__(self, name='first'):
        super().__init__(name=name)

        text1_0 = Label(text='[font=OpenSans.ttf]' + 'Вход в аккаунт' + '[/font]', markup=True, font_size='28sp',
                        pos_hint={'center_x': 0.5, 'center_y': 5})

        enter_back_stroke = EnterRoundButton()
        create_back_stroke = CreateRoundButton()

        ava = Image(source='ava.png', pos_hint={'center_x': 0.5, 'center_y': 1})

        button1_1 = Button(text='[font=OpenSans.ttf]' + 'Войти в аккаунт' + '[/font]', markup=True, font_size='20sp',
                           size_hint=(0.6, 0.3), pos_hint={'center_x': 0.5})
        button1_1.background_color = (0, 0, 0, 0)
        button1_1.on_press = self.next_signin

        button1_2 = Button(text='[font=OpenSans.ttf]' + 'Создать аккаунт' + '[/font]', markup=True, font_size='20sp',
                           size_hint=(0.6, 0.3), pos_hint={'center_x': 0.5})
        button1_2.background_color = (0, 0, 0, 0)
        button1_2.on_press = self.next_login

        layout_v_text = BoxLayout(orientation='vertical', spacing=4, padding=8,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.9})
        layout_v_back = BoxLayout(orientation='vertical')
        layout_v_buttons = BoxLayout(orientation='vertical', spacing=11, padding=10,
                                     pos_hint={'center_x': 0.5, 'center_y': 0.709})
        layout_v_ava = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.65})

        layout_v_back.add_widget(enter_back_stroke)
        layout_v_back.add_widget(create_back_stroke)

        space1 = Label(text='')
        space2 = Label(text='')

        layout_v_text.add_widget(text1_0)
        layout_v_ava.add_widget(ava)

        layout_v_buttons.add_widget(space1)
        layout_v_buttons.add_widget(space2)
        layout_v_buttons.add_widget(button1_1)
        layout_v_buttons.add_widget(button1_2)

        self.add_widget(layout_v_back)
        self.add_widget(layout_v_text)
        self.add_widget(layout_v_ava)
        self.add_widget(layout_v_buttons)

    def next_signin(self):
        self.manager.current = 'signin'
        self.manager.transition.direction = 'left'

    def next_login(self):
        self.manager.current = 'login'
        self.manager.transition.direction = 'left'


class SignIn(Screen):
    def __init__(self, name='signin'):
        super().__init__(name=name)

        text2_0 = Label(text='[font=OpenSans.ttf]' + 'Вход в аккаунт' + '[/font]', markup=True, font_size='28sp')

        text2_1 = Label(text='[font=OpenSans.ttf]' + 'Ваш логин или e-mail' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))
        text2_2 = Label(text='[font=OpenSans.ttf]' + 'Ваш пароль' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))
        self.text_input_login = TextInput(halign='left', focus=False, multiline=False, background_color=(0, 0, 0, 0),
                                          size_hint=(0.85, 0.2), pos_hint={'center_x': 0.5})
        self.text_input_password = TextInput(halign='left', focus=False, multiline=False, background_color=(0, 0, 0, 0),
                                             password=True, size_hint=(0.85, 0.2), pos_hint={'center_x': 0.5})

        button2_1 = Button(text='[font=OpenSans.ttf]' + 'Войти в аккаунт' + '[/font]', markup=True, font_size='20sp',
                           size_hint=(0.6, 0.3), pos_hint={'center_x': 0.5})
        button2_1.background_color = (0, 0, 0, 0)
        button2_1.on_press = self.next
        button2_2 = Button(text='[font=OpenSans.ttf]' + 'Забыли пароль?' + '[/font]', markup=True, font_size='20sp',
                           size_hint=(0.6, 0.3), pos_hint={'center_x': 0.5})
        button2_2.background_color = (0, 0, 0, 0)
        button2_2.on_press = self.reset

        input_login_background = InputBackground()
        input_password_background = InputBackground()
        layout_v_input_login = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.35})
        layout_v_input_password = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.2})
        layout_v_input_login.add_widget(input_login_background)
        space1 = Label(text='')
        space2 = Label(text='')
        space3 = Label(text='')
        space4 = Label(text='')
        layout_v_input_login.add_widget(space1)
        layout_v_input_login.add_widget(space2)
        layout_v_input_login.add_widget(space3)
        layout_v_input_login.add_widget(space4)
        layout_v_input_password.add_widget(input_password_background)
        space1_2 = Label(text='')
        space2_2 = Label(text='')
        space3_2 = Label(text='')
        space4_2 = Label(text='')
        layout_v_input_password.add_widget(space1_2)
        layout_v_input_password.add_widget(space2_2)
        layout_v_input_password.add_widget(space3_2)
        layout_v_input_password.add_widget(space4_2)

        enter_back_stroke = EnterRoundButton()
        create_back_stroke = ForgotPasswordRoundButton()
        layout_v_back = BoxLayout(orientation='vertical')
        layout_v_back.add_widget(enter_back_stroke)
        layout_v_back.add_widget(create_back_stroke)

        space1 = Label(text='')
        space2 = Label(text='')
        layout_v_buttons = BoxLayout(orientation='vertical', spacing=11, padding=10,
                                     pos_hint={'center_x': 0.5, 'center_y': 0.709})
        layout_v_buttons.add_widget(space1)
        layout_v_buttons.add_widget(space2)
        layout_v_buttons.add_widget(button2_1)
        layout_v_buttons.add_widget(button2_2)

        layout_v_text = BoxLayout(orientation='vertical', spacing=4, padding=8,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.9})
        layout_v_text.add_widget(text2_0)

        arrow_back = ArrowButton()
        back = ScrButton(self, text='', direction='right', goal='first', background_color=(0, 0, 0, 0),
                         size_hint=(0.2, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout_v_back_button = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.1, 'center_y': 1.3})
        layout_v_back_button.add_widget(arrow_back)
        layout_v_back_button.add_widget(back)

        layout_input_text_login = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.3, 'center_y': 0.475})
        layout_input_text_login.add_widget(text2_1)
        space5 = Label(text='')
        space6 = Label(text='')
        layout_input_text_login.add_widget(space5)
        layout_input_text_login.add_widget(space6)
        layout_input_text_password = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.21, 'center_y': 0.325})
        layout_input_text_password.add_widget(text2_2)
        space7 = Label(text='')
        space8 = Label(text='')
        layout_input_text_password.add_widget(space7)
        layout_input_text_password.add_widget(space8)

        layout_v_main_inputs = BoxLayout(orientation='vertical', pos_hint={'center_y': 0.277}, spacing=53)
        layout_v_main_inputs.add_widget(self.text_input_login)
        layout_v_main_inputs.add_widget(self.text_input_password)
        space9 = Label(text='')
        space10 = Label(text='')
        layout_v_main_inputs.add_widget(space9)
        layout_v_main_inputs.add_widget(space10)

        self.add_widget(layout_v_back_button)
        self.add_widget(layout_v_input_login)
        self.add_widget(layout_v_input_password)
        self.add_widget(layout_input_text_login)
        self.add_widget(layout_input_text_password)
        self.add_widget(layout_v_back)
        self.add_widget(layout_v_text)
        self.add_widget(layout_v_main_inputs)
        self.add_widget(layout_v_buttons)

    def next(self):
        if self.text_input_login.text != '' and self.text_input_password.text != '':
            global user_email, user_login, user_password
            user_login = self.text_input_login.text
            user_password = self.text_input_password.text
            self.manager.current = 'main'
            self.manager.transition.direction = 'left'
            self.text_input_password.text = ''
        else:
            popup_layout = BoxLayout(orientation='horizontal')
            popup_button_close = Button(text='Закрыть', pos_hint={'center_y': .4}, size_hint=(0.3, 0.8),
                                        background_color=button_color)
            popup_layout.add_widget(popup_button_close)
            self.popup = Popup(title='Необходимо заполнить все данные!', content=popup_layout, size_hint=(0.4, 0.2),
                               auto_dismiss=False)
            self.popup.open()
            popup_button_close.bind(on_press=self.popup.dismiss)

    def reset(self):
        self.manager.current = 'password_reset'

        self.text_input_password.text = ''


class LogIn(Screen):
    def __init__(self, name='login'):
        super().__init__(name=name)

        text3_0 = Label(text='[font=OpenSans.ttf]' + 'Создание аккаунта' + '[/font]', markup=True, font_size='28sp')
        layout_v_text = BoxLayout(orientation='vertical', spacing=4, padding=8,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.9})
        layout_v_text.add_widget(text3_0)

        arrow_back = ArrowButton()
        back = ScrButton(self, text='', direction='right', goal='first', background_color=(0, 0, 0, 0),
                         size_hint=(0.2, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout_v_back_button = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.1, 'center_y': 1.3})
        layout_v_back_button.add_widget(arrow_back)
        layout_v_back_button.add_widget(back)

        input_email_background = InputBackground()
        input_login_background = InputBackground()
        layout_v_input_email = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.35})
        layout_v_input_login = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.2})
        layout_v_input_email.add_widget(input_email_background)
        space1 = Label(text='')
        space2 = Label(text='')
        space3 = Label(text='')
        space4 = Label(text='')
        layout_v_input_email.add_widget(space1)
        layout_v_input_email.add_widget(space2)
        layout_v_input_email.add_widget(space3)
        layout_v_input_email.add_widget(space4)
        layout_v_input_login.add_widget(input_login_background)
        space1_2 = Label(text='')
        space2_2 = Label(text='')
        space3_2 = Label(text='')
        space4_2 = Label(text='')
        layout_v_input_login.add_widget(space1_2)
        layout_v_input_login.add_widget(space2_2)
        layout_v_input_login.add_widget(space3_2)
        layout_v_input_login.add_widget(space4_2)
        input_password_background = InputBackground()
        input_again_password_background = InputBackground()
        layout_v_input_password = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.05})
        layout_v_input_again_password = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': -0.1})
        layout_v_input_password.add_widget(input_password_background)
        space1_3 = Label(text='')
        space2_3 = Label(text='')
        space3_3 = Label(text='')
        space4_3 = Label(text='')
        layout_v_input_password.add_widget(space1_3)
        layout_v_input_password.add_widget(space2_3)
        layout_v_input_password.add_widget(space3_3)
        layout_v_input_password.add_widget(space4_3)
        layout_v_input_again_password.add_widget(input_again_password_background)
        space1_4 = Label(text='')
        space2_4 = Label(text='')
        space3_4 = Label(text='')
        space4_4 = Label(text='')
        layout_v_input_again_password.add_widget(space1_4)
        layout_v_input_again_password.add_widget(space2_4)
        layout_v_input_again_password.add_widget(space3_4)
        layout_v_input_again_password.add_widget(space4_4)

        create_button_back_stroke = EnterRoundButton()
        just_nothing = EnterRoundButton()
        layout_v_create_button = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.25})
        layout_v_create_button.add_widget(create_button_back_stroke)
        layout_v_create_button.add_widget(just_nothing)

        button4_1 = Button(text='[font=OpenSans.ttf]' + 'Создать аккаунт' + '[/font]', markup=True, font_size='20sp',
                           size_hint=(0.6, 0.3), pos_hint={'center_x': 0.5})
        button4_1.background_color = (0, 0, 0, 0)
        button4_1.on_press = self.next
        layout_main_button = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.585})
        space1_5 = Label(text='')
        space2_5 = Label(text='')
        layout_main_button.add_widget(space1_5)
        layout_main_button.add_widget(space2_5)
        layout_main_button.add_widget(button4_1)

        self.text_input_email = TextInput(halign='left', focus=False, multiline=False, background_color=(0, 0, 0, 0),
                                          size_hint=(0.85, 0.16), pos_hint={'center_x': 0.5})
        self.text_input_login = TextInput(halign='left', focus=False, multiline=False, background_color=(0, 0, 0, 0),
                                          size_hint=(0.85, 0.16), pos_hint={'center_x': 0.5})
        self.text_input_password = TextInput(halign='left', focus=False, multiline=False, background_color=(0, 0, 0, 0),
                                             size_hint=(0.85, 0.16), pos_hint={'center_x': 0.5}, password=True)
        self.text_input_again_password = TextInput(halign='left', focus=False, multiline=False,
                                                   background_color=(0, 0, 0, 0), size_hint=(0.85, 0.16),
                                                   pos_hint={'center_x': 0.5}, password=True)

        layout_v_main_inputs = BoxLayout(orientation='vertical', pos_hint={'center_y': 0.277}, spacing=51.5)
        layout_v_main_inputs.add_widget(self.text_input_email)
        layout_v_main_inputs.add_widget(self.text_input_login)
        layout_v_main_inputs.add_widget(self.text_input_password)
        layout_v_main_inputs.add_widget(self.text_input_again_password)
        space9 = Label(text='')
        layout_v_main_inputs.add_widget(space9)

        text3_1 = Label(text='[font=OpenSans.ttf]' + 'Ваш e-mail' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))
        text3_2 = Label(text='[font=OpenSans.ttf]' + 'Ваш логин' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))
        text3_3 = Label(text='[font=OpenSans.ttf]' + 'Ваш пароль' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))
        text3_4 = Label(text='[font=OpenSans.ttf]' + 'Подтвердить пароль' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))

        layout_input_text_email = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.21, 'center_y': 0.475})
        layout_input_text_email.add_widget(text3_1)
        space11 = Label(text='')
        space22 = Label(text='')
        layout_input_text_email.add_widget(space11)
        layout_input_text_email.add_widget(space22)
        layout_input_text_login = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.21, 'center_y': 0.325})
        layout_input_text_login.add_widget(text3_2)
        space33 = Label(text='')
        space44 = Label(text='')
        layout_input_text_login.add_widget(space33)
        layout_input_text_login.add_widget(space44)
        layout_input_text_password = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.21, 'center_y': 0.175})
        layout_input_text_password.add_widget(text3_3)
        space55 = Label(text='')
        space66 = Label(text='')
        layout_input_text_password.add_widget(space55)
        layout_input_text_password.add_widget(space66)
        layout_input_text_again_password = BoxLayout(orientation='vertical',
                                                     pos_hint={'center_x': 0.3, 'center_y': 0.025})
        layout_input_text_again_password.add_widget(text3_4)
        space77 = Label(text='')
        space88 = Label(text='')
        layout_input_text_again_password.add_widget(space77)
        layout_input_text_again_password.add_widget(space88)

        self.add_widget(layout_v_create_button)
        self.add_widget(layout_v_input_email)
        self.add_widget(layout_v_input_login)
        self.add_widget(layout_v_input_password)
        self.add_widget(layout_v_input_again_password)
        self.add_widget(layout_v_back_button)
        self.add_widget(layout_input_text_email)
        self.add_widget(layout_input_text_login)
        self.add_widget(layout_input_text_password)
        self.add_widget(layout_input_text_again_password)
        self.add_widget(layout_main_button)
        self.add_widget(layout_v_main_inputs)
        self.add_widget(layout_v_text)

    def next(self):
        if self.text_input_email.text != '' and self.text_input_login.text != '' and self.text_input_password.text != '' and self.text_input_again_password.text != '':
            if self.text_input_password.text == self.text_input_again_password.text:
                self.manager.current = 'main'
                self.manager.transition.direction = 'left'
                global user_email
                global user_login
                global user_password
                user_login = self.text_input_login.text
                user_password = self.text_input_password.text
                user_email = self.text_input_email.text

                app.sm.get_screen('profile').text_input_email.text = self.text_input_email.text
                app.sm.get_screen('profile').text_input_login.text = self.text_input_login.text

                self.text_input_email.text = ''
                self.text_input_login.text = ''
                self.text_input_password.text = ''
                self.text_input_again_password.text = ''
            else:
                popup_layout = BoxLayout(orientation='horizontal')
                popup_button_close = Button(text='Закрыть', pos_hint={'center_y': .4}, size_hint=(0.3, 0.8),
                                            background_color=button_color)
                popup_layout.add_widget(popup_button_close)
                self.popup = Popup(title='Введенные пароли не совпадают!', content=popup_layout, size_hint=(0.4, 0.2),
                                   auto_dismiss=False)
                self.popup.open()
                popup_button_close.bind(on_press=self.popup.dismiss)
        else:
            popup_layout = BoxLayout(orientation='horizontal')
            popup_button_close = Button(text='Закрыть', pos_hint={'center_y': .4}, size_hint=(0.3, 0.8),
                                        background_color=button_color)
            popup_layout.add_widget(popup_button_close)
            self.popup = Popup(title='Необходимо заполнить все данные!', content=popup_layout, size_hint=(0.4, 0.2),
                               auto_dismiss=False)
            self.popup.open()
            popup_button_close.bind(on_press=self.popup.dismiss)


class Reset_Password(Screen):
    def __init__(self, name='password_reset'):
        super().__init__(name=name)

        text4_0 = Label(text='[font=OpenSans.ttf]' + 'Сброс пароля' + '[/font]', markup=True, font_size='28sp')
        text4_1 = Label(text='[font=OpenSans.ttf]' + 'Ваш e-mail' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))
        text_input_login = TextInput(halign='left', focus=False, multiline=False, background_color=(0, 0, 0, 0),
                                     size_hint=(0.85, 0.2), pos_hint={'center_x': 0.5})
        button4_1 = Button(text='[font=OpenSans.ttf]' + 'Сбросить пароль' + '[/font]', markup=True, font_size='20sp',
                           size_hint=(0.6, 0.28), pos_hint={'center_x': 0.5})
        button4_1.background_color = (0, 0, 0, 0)

        reset_back_stroke = ResetRoundButton()
        reset_again_back_stroke = ResetAgainButton()
        layout_v_back = BoxLayout(orientation='vertical')
        layout_v_back.add_widget(reset_back_stroke)
        layout_v_back.add_widget(reset_again_back_stroke)

        layout_v = BoxLayout(orientation='vertical')

        # layout_v.add_widget(text4_0)
        # layout_v.add_widget(text4_1)
        # layout_v.add_widget(text_input4_1)
        # layout_v.add_widget(button4_1)

        arrow_back = ArrowButton()
        back = ScrButton(self, text='', direction='right', goal='signin', background_color=(0, 0, 0, 0),
                         size_hint=(0.2, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout_v_back_button = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.1, 'center_y': 1.3})
        layout_v_back_button.add_widget(arrow_back)
        layout_v_back_button.add_widget(back)

        layout_v_text = BoxLayout(orientation='vertical', spacing=4, padding=8,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.9})
        layout_v_text.add_widget(text4_0)

        space1 = Label(text='')
        space2 = Label(text='')
        layout_v_buttons = BoxLayout(orientation='vertical', spacing=11, padding=10,
                                     pos_hint={'center_x': 0.5, 'center_y': 0.83})
        layout_v_buttons.add_widget(space1)
        layout_v_buttons.add_widget(space2)
        layout_v_buttons.add_widget(button4_1)

        input_login_background = InputBackground()
        layout_v_input_login = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.35})
        layout_v_input_login.add_widget(input_login_background)
        space1 = Label(text='')
        space2 = Label(text='')
        space3 = Label(text='')
        space4 = Label(text='')
        layout_v_input_login.add_widget(space1)
        layout_v_input_login.add_widget(space2)
        layout_v_input_login.add_widget(space3)
        layout_v_input_login.add_widget(space4)

        layout_input_text_login = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.21, 'center_y': 0.475})
        layout_input_text_login.add_widget(text4_1)
        space5 = Label(text='')
        space6 = Label(text='')
        layout_input_text_login.add_widget(space5)
        layout_input_text_login.add_widget(space6)

        layout_v_main_inputs = BoxLayout(orientation='vertical', pos_hint={'center_y': 0.276}, spacing=53)
        layout_v_main_inputs.add_widget(text_input_login)
        space9 = Label(text='')
        space10 = Label(text='')
        space11 = Label(text='')
        layout_v_main_inputs.add_widget(space9)
        layout_v_main_inputs.add_widget(space10)
        layout_v_main_inputs.add_widget(space11)

        self.add_widget(layout_v_back_button)
        self.add_widget(layout_v_input_login)
        self.add_widget(layout_v)
        self.add_widget(layout_v_back)
        self.add_widget(layout_v_text)
        self.add_widget(layout_input_text_login)
        self.add_widget(layout_v_main_inputs)
        self.add_widget(layout_v_buttons)


###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################
###################################################################################################################################################


# SearchButtonBackground

class Main(Screen):
    def __init__(self, name='main'):
        super().__init__(name=name)

        panel_foreground_layout = FloatLayout()
        panel_foreground_layout_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.125),
                                                pos_hint={'center_x': 0.5, 'center_y': 0.06})
        timer_button = Button(background_color=(0, 0, 0, 0))
        timer_button.on_press = self.go_timer
        statistics_button = Button(background_color=(0, 0, 0, 0))
        statistics_button.on_press = self.go_stats
        plus_button = Button(size_hint=(1, 1.2), background_color=(0, 0, 0, 0))
        plus_button.on_press = self.go_create
        profile_button = Button(background_color=(0, 0, 0, 0))
        profile_button.on_press = self.go_profile
        settings_button = Button(background_color=(0, 0, 0, 0))
        settings_button.on_press = self.go_settings
        panel_foreground_layout_box.add_widget(timer_button)
        panel_foreground_layout_box.add_widget(statistics_button)
        panel_foreground_layout_box.add_widget(plus_button)
        panel_foreground_layout_box.add_widget(profile_button)
        panel_foreground_layout_box.add_widget(settings_button)
        panel_foreground_layout.add_widget(panel_foreground_layout_box)

        self.add_widget(panel_foreground_layout)

    def go_timer(self):
        self.manager.current = 'timer'

    def go_stats(self):
        self.manager.current = 'stats'

    def go_create(self):
        self.manager.current = 'createproject'

    def go_profile(self):
        self.manager.current = 'profile'

    def go_settings(self):
        self.manager.current = 'settings'

    def do_searching(self, query, *args):
        print(self.ids.search_text.text)
        self.ids.search_text.text = ''


'''
    def ():
        .add_widget(ProjectIconBackground())
        projects.append(self)
'''


#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################
class CreateProject(Screen):
    def __init__(self, main, name='createproject'):
        self.main = main
        super().__init__(name=name)

    def change_status_norm(self, *args):
        self.ids.selected_status_layout_background.pos_hint = {'center_x': 0.2}
        self.ids.select_status.status = (0.58, 0.65, 0.81, 1)
        global flag
        flag = 2

    def change_status_long(self, *args):
        self.ids.selected_status_layout_background.pos_hint = {'center_x': 0.5}
        self.ids.select_status.status = (0.85, 0.67, 0.21, 1)
        global flag
        flag = 3


    def change_status_short(self, *args):
        self.ids.selected_status_layout_background.pos_hint = {'center_x': 0.8}
        self.ids.select_status.status = (0.76, 0.11, 0.11, 1)
        global flag
        flag = 1

    def add_tag(self, *args):
        if self.ids.add_tag_input.text != '':
            self.ids.tag_list.add_widget(TagBackground(self,
                                                       text=self.ids.add_tag_input.text))  #####################################################################################
            global current_tags
            current_tags.append(self.ids.add_tag_input.text)
            self.ids.add_tag_input.text = ''
        else:
            self.ids.add_tag_input.text = 'Необходимо ввести тег!'

    def delete_input_text(self, *args):
        self.ids.add_tag_input.text = ''

    def tick_image_1(self, *args):
        # self.ticked_layout.pos_hint = {'center_x':0.1}
        self.ids.Img1.source = 'ticked_button.png'
        global proj_image
        proj_image = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_2(self, *args):
        self.ids.Img2.source = 'ticked_button.png'
        proj_image = '2.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_3(self, *args):
        self.ids.Img3.source = 'ticked_button.png'
        proj_image = '3.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_4(self, *args):
        self.ids.Img4.source = 'ticked_button.png'
        proj_image = '4.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_5(self, *args):
        self.ids.Img5.source = 'ticked_button.png'
        proj_image = '5.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_6(self, *args):
        self.ids.Img6.source = 'ticked_button.png'
        proj_image = '6.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_7(self, *args):
        self.ids.Img7.source = 'ticked_button.png'
        proj_image = '7.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_8(self, *args):
        self.ids.Img8.source = 'ticked_button.png'
        proj_image = '8.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_9(self, *args):
        self.ids.Img9.source = 'ticked_button.png'
        proj_image = '9.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'
        self.ids.Img15.source = '15.png'

    def tick_image_10(self, *args):
        self.ids.Img10.source = 'ticked_button.png'
        proj_image = '10.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_11(self, *args):
        self.ids.Img11.source = 'ticked_button.png'
        proj_image = '11.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_12(self, *args):
        self.ids.Img12.source = 'ticked_button.png'
        proj_image = '12.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_13(self, *args):
        self.ids.Img13.source = 'ticked_button.png'
        proj_image = '13.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

    def tick_image_14(self, *args):
        self.ids.Img14.source = 'ticked_button.png'
        proj_image = '14.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img15.source = '15.png'

    def tick_image_15(self, *args):
        self.ids.Img15.source = 'ticked_button.png'
        proj_image = '15.png'
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'

    def cancel(self, *args):
        self.manager.current = 'main'
        self.ids.selected_status_layout_background.pos_hint = {'center_x': 0.2}

        self.ids.proj_name.text = ''
        self.ids.tag_list.clear_widgets()
        self.ids.Img1.source = '1.png'
        self.ids.Img2.source = '2.png'
        self.ids.Img3.source = '3.png'
        self.ids.Img4.source = '4.png'
        self.ids.Img5.source = '5.png'
        self.ids.Img6.source = '6.png'
        self.ids.Img7.source = '7.png'
        self.ids.Img8.source = '8.png'
        self.ids.Img9.source = '9.png'
        self.ids.Img10.source = '10.png'
        self.ids.Img11.source = '11.png'
        self.ids.Img12.source = '12.png'
        self.ids.Img13.source = '13.png'
        self.ids.Img14.source = '14.png'
        self.ids.Img15.source = '15.png'

        self.ids.select_status.status = (0.58, 0.65, 0.81, 1)
        tagss.clear()

    def create(self, name, status, *args):

        if self.ids.proj_name.text != '':

            # tag_list; proj_name; all_project_tags

            if (len(project_number) % 2) == 0:
                app.add_widget_at_app(ProjectButtonScreen(name=name, my_parent=self.main))
                self.main.ids.left_box.add_widget(
                    ProjectButton(self, name=name, project_tags=tagss, tag=tagss, status=status, my_parent=self.main,
                                  goal=name))

            elif (len(project_number) % 2) == 1:
                # self.main.ids.right_box.add_widget(ProjectButton(self, name=name, project_tags = tagss, tag=tag,background_color=status, my_parent=self.main))
                app.add_widget_at_app(ProjectButtonScreen(name=name, my_parent=self.main))
                self.main.ids.right_box.add_widget(
                    ProjectButton(self, name=name, project_tags=tagss, tag=tagss, status=status, my_parent=self.main,
                                  goal=name))

            global project_number_i
            project_number.append(project_number_i)
            project_number_i += 1
            # self.main.ids.main_grid.add_widget(ProjectButton(my_parent=self.main))

            self.manager.current = 'main'
            self.ids.selected_status_layout_background.pos_hint = {'center_x': 0.2}

            self.ids.tag_list.clear_widgets()
            self.ids.Img1.source = '1.png'
            self.ids.Img2.source = '2.png'
            self.ids.Img3.source = '3.png'
            self.ids.Img4.source = '4.png'
            self.ids.Img5.source = '5.png'
            self.ids.Img6.source = '6.png'
            self.ids.Img7.source = '7.png'
            self.ids.Img8.source = '8.png'
            self.ids.Img9.source = '9.png'
            self.ids.Img10.source = '10.png'
            self.ids.Img11.source = '11.png'
            self.ids.Img12.source = '12.png'
            self.ids.Img13.source = '13.png'
            self.ids.Img14.source = '14.png'
            self.ids.Img15.source = '15.png'
            self.ids.proj_name.text = ''
            if flag == 1:
                self.ids.select_status.status = (0.58, 0.65, 0.81, 1)
            elif flag == 2:
                self.ids.select_status.status = (0.76, 0.11, 0.11, 1)
            elif flag == 3:
                self.ids.select_status.status = (0.85, 0.67, 0.21, 1)

            tagss.clear()

        else:
            print('Необходимо заполнить все параметры!')


###################################################################################################################################################
class Timer(Screen):
    def __init__(self, name='timer'):
        super().__init__(name=name)

        self.round_t_test = Base()

        space1 = Label(text='')
        space2 = Label(text='')
        space3 = Label(text='')
        space4 = Label(text='')

        self.start_button = Button(text='Начать', background_color=(0, 0, 0, 0), size_hint=(0.6, 1),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.start_button.on_press = self.begin
        # self.stop_button = Button(text='Стоп', background_color = button_color, size_hint=(1,0.2))
        # self.stop_button.on_press = self.finish
        # self.pause_button = Button(text='Пауза', background_color = (0,0,0,0), size_hint=(0.3,3.5), pos_hint={'center_x':0.5,'center_y':-1})
        # self.pause_button.on_press = self.pause
        self.round_timer = Seconds(900, background_color=(0, 0, 0, 0), size_hint=(0.7, 4),
                                   pos_hint={'center_x': 0.5, 'center_y': 1}, font_size='44sp',
                                   font_name='Roboto-Regular.ttf')
        self.round_timer.on_press = self.pause
        self.round_timer.bind(done=self.sec_finished)

        layout_v = BoxLayout(orientation='vertical', pos_hint={'center_y': 0.6})

        layout_v.add_widget(space1)
        layout_v.add_widget(space2)
        layout_v.add_widget(space4)
        # layout_v.add_widget(self.pause_button)
        layout_v.add_widget(self.round_timer)
        layout_v.add_widget(space3)
        # layout_v.add_widget(self.stop_button)
        layout_v.add_widget(self.start_button)
        layout_v.add_widget(self.round_t_test)
        back = ScrButton(self, text='назад', goal='main', background_color='red', size_hint=(0.4, 0.2),
                         pos_hint={'center_x': 0.5})
        back.bind(on_press=self.setnulstage)
        # back.nulstage()
        # layout_v_main.add_widget(layout_v)

        round_button = EnterRoundButton()
        round_button_layout = BoxLayout(orientation='vertical', size_hint=(1, 1),
                                        pos_hint={'center_x': 0.5, 'center_y': 0.85})
        space1_1 = Label(text='')
        round_button_layout.add_widget(space1_1)
        round_button_layout.add_widget(round_button)

        ############### при смене экрана во время активного таймера приравнять stage к нулю!!!!!!!!!!!!!!!!!!!!!!!!!

        self.add_widget(round_button_layout)
        self.add_widget(layout_v)
        # self.add_widget(layout_v_back)

        panel_backgroud = BottomPanelBackground_timer()
        panel_backgroud_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.125), pos_hint={'center_x': 0.5})
        panel_backgroud_layout.add_widget(panel_backgroud)

        self.add_widget(panel_backgroud_layout)

        panel_foreground_layout = FloatLayout()
        panel_foreground_layout_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.125),
                                                pos_hint={'center_x': 0.5, 'center_y': 0.06})
        timer_button = Button(background_color=(0, 0, 0, 0))
        timer_button.on_press = self.go_timer
        statistics_button = Button(background_color=(0, 0, 0, 0))
        statistics_button.on_press = self.go_stats
        home_button = Button(size_hint=(1, 1.2), background_color=(0, 0, 0, 0))
        home_button.on_press = self.go_main
        profile_button = Button(background_color=(0, 0, 0, 0))
        profile_button.on_press = self.go_profile
        settings_button = Button(background_color=(0, 0, 0, 0))
        settings_button.on_press = self.go_settings
        panel_foreground_layout_box.add_widget(timer_button)
        panel_foreground_layout_box.add_widget(statistics_button)
        panel_foreground_layout_box.add_widget(home_button)
        panel_foreground_layout_box.add_widget(profile_button)
        panel_foreground_layout_box.add_widget(settings_button)
        panel_foreground_layout.add_widget(panel_foreground_layout_box)

        self.add_widget(panel_foreground_layout)

    def go_timer(self):
        self.manager.current = 'timer'

    def go_stats(self):
        self.manager.current = 'stats'

    def go_main(self):
        self.manager.current = 'main'

    def go_profile(self):
        self.manager.current = 'profile'

    def go_settings(self):
        self.manager.current = 'settings'

    def setnulstage(self, *args):
        global stage
        stage = 0

    def begin(self, *args):
        global stage
        stage = 1
        self.start_button.text = 'Стоп'
        self.start_button.on_press = self.finish
        self.round_timer.start()
        # self.start_button.text = 'Стоп'
        self.round_timer.on_press = self.pause

    def pause(self, *args):
        self.round_timer.stop()
        global stage
        if stage == 1:
            self.round_timer.on_press = self.begin
            stage = 0
        stage = 0

    def finish(self, *args):
        # self.round_timer.restart(20)
        global stage
        stage = 0
        popup_layout = BoxLayout(orientation='horizontal')
        popup_text = Label(text='Вы уверены, что хотите остановить таймер?')
        popup_button_yes = Button(text='Стоп', pos_hint={'center_y': .4}, size_hint=(0.3, 0.8))
        popup_button_no = Button(text='Отменить', pos_hint={'center_y': .4}, size_hint=(0.3, 0.8))
        popup_layout.add_widget(popup_button_no)
        popup_layout.add_widget(popup_button_yes)
        self.timer_stop_popup = Popup(title='Вы уверены, что хотите остановить таймер?', content=popup_layout,
                                      size_hint=(0.4, 0.2), auto_dismiss=False)
        self.timer_stop_popup.open()
        popup_button_no.on_press = self.timer_stop_popup.dismiss
        stage = 1
        popup_button_yes.on_press = self.timer_stop_popup.dismiss
        popup_button_yes.bind(on_press=self.sure_finish)
        # popup_button_yes.on_press = timer_stop_popup.dismiss

    def sure_finish(self, *args):
        global stage
        stage = 0
        self.round_timer.restart(900)
        self.timer_stop_popup.dismiss
        self.start_button.text = 'Начать'
        self.start_button.on_press = self.begin

    def new_sure_finish(self, *args):
        global stage
        stage = 0
        self.round_timer.restart(900)
        self.start_button.text = 'Начать'
        self.start_button.on_press = self.begin

    def sec_finished(self, *args):
        global stage
        stage = 0
        self.round_timer.restart(900)
        self.start_button.text = 'Начать'
        self.start_button.on_press = self.begin

    def next(self):
        self.round_timer.start()


###################################################################################################################################################

class Statistics_norm(Screen):
    def __init__(self, name='stats_norm'):
        super().__init__(name=name)

        text = Label(text='статистика')
        top_mode_btn_1 = ToggleButton(text='[font=OpenSans.ttf]' + 'Неделя' + '[/font]', markup=True, font_size='14sp',
                                      group='mode', state='down', background_color=button_color)
        top_mode_btn_2 = ToggleButton(text='[font=OpenSans.ttf]' + 'Месяц' + '[/font]', markup=True, font_size='14sp',
                                      group='mode', background_color=button_color)
        top_mode_btn_3 = ToggleButton(text='[font=OpenSans.ttf]' + 'Все время' + '[/font]', markup=True,
                                      font_size='14sp', group='mode', background_color=button_color)
        # как сделать, чтобы обязательно была включена хотя бы одна
        top_toggle_layout = BoxLayout(orientation='horizontal')
        top_toggle_layout.add_widget(top_mode_btn_1)
        top_toggle_layout.add_widget(top_mode_btn_2)
        top_toggle_layout.add_widget(top_mode_btn_3)
        #####################################_первый_круг_#####################################
        stat_round_1 = Label(text='***круг 1')
        dot_1 = Label(text='*')
        dot_2 = Label(text='*')
        dot_3 = Label(text='*')
        projects = Label(text='[font=OpenSans.ttf]' + 'Проекты' + '[/font]', markup=True, font_size='14sp')
        projects_completed = Label(text='[font=OpenSans.ttf]' + ' завершено' + '[/font]', markup=True, font_size='14sp')
        tasks = Label(text='[font=OpenSans.ttf]' + 'Задачи' + '[/font]', markup=True, font_size='14sp')
        tasks_completed = Label(text='[font=OpenSans.ttf]' + ' завершено' + '[/font]', markup=True, font_size='14sp')
        working = Label(text='[font=OpenSans.ttf]' + 'В работе' + '[/font]', markup=True, font_size='14sp')
        work_hours = Label(text='[font=OpenSans.ttf]' + ' часов' + '[/font]', markup=True, font_size='14sp')
        proj_layout_v = BoxLayout(orientation='vertical')
        proj_layout_v.add_widget(projects)
        proj_layout_v.add_widget(projects_completed)
        task_layout_v = BoxLayout(orientation='vertical')
        task_layout_v.add_widget(tasks)
        task_layout_v.add_widget(tasks_completed)
        hours_layout_v = BoxLayout(orientation='vertical')
        hours_layout_v.add_widget(working)
        hours_layout_v.add_widget(work_hours)
        proj_layout_h = BoxLayout(orientation='horizontal')
        proj_layout_h.add_widget(dot_1)
        proj_layout_h.add_widget(proj_layout_v)
        tasks_layout_h = BoxLayout(orientation='horizontal')
        tasks_layout_h.add_widget(dot_2)
        tasks_layout_h.add_widget(task_layout_v)
        work_layout_h = BoxLayout(orientation='horizontal')
        work_layout_h.add_widget(dot_3)
        work_layout_h.add_widget(hours_layout_v)
        text_round_layout_v = BoxLayout(orientation='vertical')
        text_round_layout_v.add_widget(proj_layout_h)
        text_round_layout_v.add_widget(tasks_layout_h)
        text_round_layout_v.add_widget(work_layout_h)
        great_stats_1_layout_h = BoxLayout(orientation='horizontal')
        great_stats_1_layout_h.add_widget(stat_round_1)
        great_stats_1_layout_h.add_widget(text_round_layout_v)
        #####################################_второй_круг_#####################################
        stat_round_2 = Label(text='***круг 2')
        dot_4 = Label(text='*')
        dot_5 = Label(text='*')
        dot_6 = Label(text='*')
        completed = Label(text='[font=OpenSans.ttf]' + 'Выполнено' + '[/font]', markup=True, font_size='14sp')
        ahead_of_schedule = Label(text='[font=OpenSans.ttf]' + ' раньше срока' + '[/font]', markup=True,
                                  font_size='14sp')
        interrupted = Label(text='[font=OpenSans.ttf]' + 'Прервано' + '[/font]', markup=True, font_size='14sp')
        delayed = Label(text='[font=OpenSans.ttf]' + ' с задержкой' + '[/font]', markup=True, font_size='14sp')
        postponed = Label(text='[font=OpenSans.ttf]' + 'Отложено' + '[/font]', markup=True, font_size='14sp')
        proj_postponed = Label(text='[font=OpenSans.ttf]' + ' проектов' + '[/font]', markup=True, font_size='14sp')
        completed_layout_v = BoxLayout(orientation='vertical')
        completed_layout_v.add_widget(completed)
        completed_layout_v.add_widget(ahead_of_schedule)
        interrupted_layout_v = BoxLayout(orientation='vertical')
        interrupted_layout_v.add_widget(interrupted)
        interrupted_layout_v.add_widget(delayed)
        later_layout_v = BoxLayout(orientation='vertical')
        later_layout_v.add_widget(postponed)
        later_layout_v.add_widget(proj_postponed)
        completed_layout_h = BoxLayout(orientation='horizontal')
        completed_layout_h.add_widget(dot_4)
        completed_layout_h.add_widget(completed_layout_v)
        interrupted_layout_h = BoxLayout(orientation='horizontal')
        interrupted_layout_h.add_widget(dot_5)
        interrupted_layout_h.add_widget(interrupted_layout_v)
        later_layout_h = BoxLayout(orientation='horizontal')
        later_layout_h.add_widget(dot_6)
        later_layout_h.add_widget(later_layout_v)
        text_round_2_layout_v = BoxLayout(orientation='vertical')
        text_round_2_layout_v.add_widget(completed_layout_h)
        text_round_2_layout_v.add_widget(interrupted_layout_h)
        text_round_2_layout_v.add_widget(later_layout_h)
        great_stats_2_layout_h = BoxLayout(orientation='horizontal')
        great_stats_2_layout_h.add_widget(stat_round_2)
        great_stats_2_layout_h.add_widget(text_round_2_layout_v)
        #####################################_График_#####################################

        #####################################_Топ_Проектов_#####################################

        #########################################################################################################

        tap_layout = BoxLayout(orientation='horizontal')
        tap_button_1 = Button(text='Кнопка 1')
        tap_button_2 = Button(text='Кнопка 2')
        tap_layout.add_widget(tap_button_1)
        tap_layout.add_widget(tap_button_2)
        week_tap_bar = TabbedPanel(default_tab_text='Неделя', default_tab_content=tap_layout)
        tap_bar_month = TabbedPanelHeader(text='Месяц')
        tap_bar_all_time = TabbedPanelHeader(text='Все время')

        week_tap_bar.add_widget(tap_bar_month)
        week_tap_bar.add_widget(tap_bar_all_time)

        layout_v = BoxLayout(orientation='vertical')
        self.layout_v_scroll = BoxLayout(orientation='vertical', size_hint_y=None)
        self.layout_v_scroll.add_widget(great_stats_1_layout_h)
        self.layout_v_scroll.add_widget(great_stats_2_layout_h)

        self.all_screen_scroll = ScrollView(size_hint=(1, 1))
        self.all_screen_scroll.add_widget(self.layout_v_scroll)

        layout_v.add_widget(text)
        layout_v.add_widget(top_toggle_layout)
        # layout_v.add_widget(great_stats_1_layout_h)
        # layout_v.add_widget(great_stats_2_layout_h)
        layout_v.add_widget(self.all_screen_scroll)

        layout_v.add_widget(week_tap_bar)

        self.add_widget(layout_v)

        panel_backgroud = BottomPanelBackground_stats()
        panel_backgroud_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.125), pos_hint={'center_x': 0.5})
        panel_backgroud_layout.add_widget(panel_backgroud)

        self.add_widget(panel_backgroud_layout)

        panel_foreground_layout = FloatLayout()
        panel_foreground_layout_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.125),
                                                pos_hint={'center_x': 0.5, 'center_y': 0.06})
        timer_button = Button(background_color=(0, 0, 0, 0))
        timer_button.on_press = self.go_timer
        statistics_button = Button(background_color=(0, 0, 0, 0))
        statistics_button.on_press = self.go_stats
        home_button = Button(size_hint=(1, 1.2), background_color=(0, 0, 0, 0))
        home_button.on_press = self.go_main
        profile_button = Button(background_color=(0, 0, 0, 0))
        profile_button.on_press = self.go_profile
        settings_button = Button(background_color=(0, 0, 0, 0))
        settings_button.on_press = self.go_settings
        panel_foreground_layout_box.add_widget(timer_button)
        panel_foreground_layout_box.add_widget(statistics_button)
        panel_foreground_layout_box.add_widget(home_button)
        panel_foreground_layout_box.add_widget(profile_button)
        panel_foreground_layout_box.add_widget(settings_button)
        panel_foreground_layout.add_widget(panel_foreground_layout_box)

        self.add_widget(panel_foreground_layout)

    def go_timer(self):
        self.manager.current = 'timer'

    def go_stats(self):
        self.manager.current = 'stats'

    def go_main(self):
        self.manager.current = 'main'

    def go_profile(self):
        self.manager.current = 'profile'

    def go_settings(self):
        self.manager.current = 'settings'


class Statistics(Screen):
    def __init__(self, name='stats'):
        super().__init__(name=name)

        img = Image(source='background_stats.png')
        text = Label(text='[font=OpenSans.ttf]' + 'Раздел находится в разработке' + '[/font]', markup=True,
                     font_size='20sp', color=(0.36, 0.39, 0.43, 1))
        text_layout = BoxLayout(pos_hint={'center_x': 0.5, 'center_y': 0.9})
        text_layout.add_widget(text)
        self.add_widget(text_layout)
        self.add_widget(img)

        panel_backgroud = BottomPanelBackground_stats()
        panel_backgroud_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.125), pos_hint={'center_x': 0.5})
        panel_backgroud_layout.add_widget(panel_backgroud)

        self.add_widget(panel_backgroud_layout)

        panel_foreground_layout = FloatLayout()
        panel_foreground_layout_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.125),
                                                pos_hint={'center_x': 0.5, 'center_y': 0.06})
        timer_button = Button(background_color=(0, 0, 0, 0))
        timer_button.on_press = self.go_timer
        statistics_button = Button(background_color=(0, 0, 0, 0))
        statistics_button.on_press = self.go_stats
        home_button = Button(size_hint=(1, 1.2), background_color=(0, 0, 0, 0))
        home_button.on_press = self.go_main
        profile_button = Button(background_color=(0, 0, 0, 0))
        profile_button.on_press = self.go_profile
        settings_button = Button(background_color=(0, 0, 0, 0))
        settings_button.on_press = self.go_settings
        panel_foreground_layout_box.add_widget(timer_button)
        panel_foreground_layout_box.add_widget(statistics_button)
        panel_foreground_layout_box.add_widget(home_button)
        panel_foreground_layout_box.add_widget(profile_button)
        panel_foreground_layout_box.add_widget(settings_button)
        panel_foreground_layout.add_widget(panel_foreground_layout_box)

        self.add_widget(panel_foreground_layout)

    def go_timer(self):
        self.manager.current = 'timer'

    def go_stats(self):
        self.manager.current = 'stats'

    def go_main(self):
        self.manager.current = 'main'

    def go_profile(self):
        self.manager.current = 'profile'

    def go_settings(self):
        self.manager.current = 'settings'


####################################################################################################################################################

class Profile(Screen):
    def __init__(self, name='profile'):
        super().__init__(name=name)

        text_0 = Label(text='[font=OpenSans.ttf]' + 'Ваш аккаунт' + '[/font]', markup=True, font_size='28sp')
        layout_v_text = BoxLayout(orientation='vertical', spacing=4, padding=8,
                                  pos_hint={'center_x': 0.5, 'center_y': 0.9})
        layout_v_text.add_widget(text_0)

        input_email_background = InputBackground()
        input_login_background = InputBackground()
        layout_v_input_email = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.35})
        layout_v_input_login = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.2})
        layout_v_input_email.add_widget(input_email_background)
        space1 = Label(text='')
        space2 = Label(text='')
        space3 = Label(text='')
        space4 = Label(text='')
        layout_v_input_email.add_widget(space1)
        layout_v_input_email.add_widget(space2)
        layout_v_input_email.add_widget(space3)
        layout_v_input_email.add_widget(space4)
        layout_v_input_login.add_widget(input_login_background)
        space1_2 = Label(text='')
        space2_2 = Label(text='')
        space3_2 = Label(text='')
        space4_2 = Label(text='')
        layout_v_input_login.add_widget(space1_2)
        layout_v_input_login.add_widget(space2_2)
        layout_v_input_login.add_widget(space3_2)
        layout_v_input_login.add_widget(space4_2)
        input_password_background = InputBackground()
        input_change_password_background = InputBackground()
        layout_v_input_password = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.05})
        layout_v_input_change_password = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': -0.1})
        layout_v_input_password.add_widget(input_password_background)
        space1_3 = Label(text='')
        space2_3 = Label(text='')
        space3_3 = Label(text='')
        space4_3 = Label(text='')
        layout_v_input_password.add_widget(space1_3)
        layout_v_input_password.add_widget(space2_3)
        layout_v_input_password.add_widget(space3_3)
        layout_v_input_password.add_widget(space4_3)
        layout_v_input_change_password.add_widget(input_change_password_background)
        space1_4 = Label(text='')
        space2_4 = Label(text='')
        space3_4 = Label(text='')
        space4_4 = Label(text='')
        layout_v_input_change_password.add_widget(space1_4)
        layout_v_input_change_password.add_widget(space2_4)
        layout_v_input_change_password.add_widget(space3_4)
        layout_v_input_change_password.add_widget(space4_4)

        ava = Image(source='ava.png', pos_hint={'center_x': 0.5, 'center_y': 1})
        layout_v_ava = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.75})
        layout_v_ava.add_widget(ava)

        text3_1 = Label(text='[font=OpenSans.ttf]' + 'Ваш e-mail' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))
        text3_2 = Label(text='[font=OpenSans.ttf]' + 'Ваш логин' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))
        text3_3 = Label(text='[font=OpenSans.ttf]' + 'Ваш пароль' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))
        text3_4 = Label(text='[font=OpenSans.ttf]' + 'Изменить пароль' + '[/font]', markup=True, font_size='14sp',
                        color=(0.36, 0.39, 0.43, 1))

        layout_input_text_email = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.21, 'center_y': 0.475})
        layout_input_text_email.add_widget(text3_1)
        space11 = Label(text='')
        space22 = Label(text='')
        layout_input_text_email.add_widget(space11)
        layout_input_text_email.add_widget(space22)
        layout_input_text_login = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.21, 'center_y': 0.325})
        layout_input_text_login.add_widget(text3_2)
        space33 = Label(text='')
        space44 = Label(text='')
        layout_input_text_login.add_widget(space33)
        layout_input_text_login.add_widget(space44)
        layout_input_text_password = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.21, 'center_y': 0.175})
        layout_input_text_password.add_widget(text3_3)
        space55 = Label(text='')
        space66 = Label(text='')
        layout_input_text_password.add_widget(space55)
        layout_input_text_password.add_widget(space66)

        global user_email, user_login, user_password

        self.text_input_email = TextInput(halign='left', focus=False, multiline=False, background_color=(0, 0, 0, 0),
                                          size_hint=(0.85, 0.2), pos_hint={'center_x': 0.5})
        self.text_input_login = TextInput(halign='left', focus=False, multiline=False, background_color=(0, 0, 0, 0),
                                          password=False, size_hint=(0.85, 0.2), pos_hint={'center_x': 0.5})

        layout_v_main_inputs = BoxLayout(orientation='vertical', pos_hint={'center_y': 0.277}, spacing=53)
        layout_v_main_inputs.add_widget(self.text_input_email)
        layout_v_main_inputs.add_widget(self.text_input_login)
        space9 = Label(text='')
        space10 = Label(text='')
        layout_v_main_inputs.add_widget(space9)
        layout_v_main_inputs.add_widget(space10)

        layout_v_change_password = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.45})
        password_change = Button(text='[font=OpenSans.ttf]' + 'Изменить пароль' + '[/font]', markup=True,
                                 font_size='14sp', background_color=(0, 0, 0, 0), size_hint=(0.9, 0.15),
                                 pos_hint={'center_x': 0.5})
        password_change.on_press = self.changepass
        space_1 = Label(text='')
        space_2 = Label(text='')
        layout_v_change_password.add_widget(space_1)
        layout_v_change_password.add_widget(password_change)
        layout_v_change_password.add_widget(space_2)

        layout_v_exit = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.3})
        exit_button = Button(
            text='[font=OpenSans.ttf]' + '[color=#FF0404]' + 'Выйти из аккаунта' + '[/color]' + '[/font]', markup=True,
            font_size='14sp', background_color=(0, 0, 0, 0), size_hint=(0.9, 0.15), pos_hint={'center_x': 0.5})
        exit_button.on_press = self.do_exit
        space_1 = Label(text='')
        space_2 = Label(text='')
        layout_v_exit.add_widget(space_1)
        layout_v_exit.add_widget(exit_button)
        layout_v_exit.add_widget(space_2)

        self.add_widget(layout_v_input_email)
        self.add_widget(layout_v_input_login)
        self.add_widget(layout_v_input_password)
        self.add_widget(layout_v_input_change_password)
        self.add_widget(layout_input_text_email)
        self.add_widget(layout_input_text_login)
        self.add_widget(layout_input_text_password)
        self.add_widget(layout_v_main_inputs)
        self.add_widget(layout_v_change_password)
        self.add_widget(layout_v_exit)
        self.add_widget(layout_v_text)
        # self.add_widget(layout_v_ava)

        panel_backgroud = BottomPanelBackground_profile()
        panel_backgroud_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.125), pos_hint={'center_x': 0.5})
        panel_backgroud_layout.add_widget(panel_backgroud)

        self.add_widget(panel_backgroud_layout)

        panel_foreground_layout = FloatLayout()
        panel_foreground_layout_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.125),
                                                pos_hint={'center_x': 0.5, 'center_y': 0.06})
        timer_button = Button(background_color=(0, 0, 0, 0))
        timer_button.on_press = self.go_timer
        statistics_button = Button(background_color=(0, 0, 0, 0))
        statistics_button.on_press = self.go_stats
        home_button = Button(size_hint=(1, 1.2), background_color=(0, 0, 0, 0))
        home_button.on_press = self.go_main
        profile_button = Button(background_color=(0, 0, 0, 0))
        profile_button.on_press = self.go_profile
        settings_button = Button(background_color=(0, 0, 0, 0))
        settings_button.on_press = self.go_settings
        panel_foreground_layout_box.add_widget(timer_button)
        panel_foreground_layout_box.add_widget(statistics_button)
        panel_foreground_layout_box.add_widget(home_button)
        panel_foreground_layout_box.add_widget(profile_button)
        panel_foreground_layout_box.add_widget(settings_button)
        panel_foreground_layout.add_widget(panel_foreground_layout_box)

        self.add_widget(panel_foreground_layout)

    def go_timer(self):
        self.manager.current = 'timer'

    def go_stats(self):
        self.manager.current = 'stats'

    def go_main(self):
        self.manager.current = 'main'

    def go_profile(self):
        self.manager.current = 'profile'

    def go_settings(self):
        self.manager.current = 'settings'

    def do_exit(self):
        self.manager.current = 'first'
        self.manager.transition.direction = 'right'

    def changepass(self, *args):
        pass


####################################################################################################################################################

class Settings_1(Screen):
    def __init__(self, name='settings'):
        super().__init__(name=name)

        text_0 = Label(text='[font=OpenSans.ttf]' + 'Настройки' + '[/font]', markup=True, font_size='28sp')
        text_1 = Label(text='[font=OpenSans.ttf]' + 'Общее' + '[/font]', markup=True, font_size='14sp')
        notif_button = Button(text='[font=OpenSans.ttf]' + 'Уведомления' + '[/font]', markup=True, font_size='14sp',
                              background_color=light_grey)
        genset_button = Button(text='[font=OpenSans.ttf]' + 'Общие настройки' + '[/font]', markup=True,
                               font_size='14sp', background_color=light_grey)
        timerset_button = Button(text='[font=OpenSans.ttf]' + 'Настройки таймера' + '[/font]', markup=True,
                                 font_size='14sp', background_color=light_grey)
        text_2 = Label(text='[font=OpenSans.ttf]' + 'Оформление' + '[/font]', markup=True, font_size='14sp')
        icon_button = Button(text='[font=OpenSans.ttf]' + 'Иконка приложения' + '[/font]', markup=True,
                             font_size='14sp', background_color=light_grey)
        theme_button = Button(text='[font=OpenSans.ttf]' + 'Тема' + '[/font]', markup=True, font_size='14sp',
                              background_color=light_grey)
        sound_button = Button(text='[font=OpenSans.ttf]' + 'Звук' + '[/font]', markup=True, font_size='14sp',
                              background_color=light_grey)
        text_3 = Label(text='[font=OpenSans.ttf]' + 'Поддержка' + '[/font]', markup=True, font_size='14sp')
        news_button = Button(text='[font=OpenSans.ttf]' + 'Что нового' + '[/font]', markup=True, font_size='14sp',
                             background_color=light_grey)
        guide_button = Button(text='[font=OpenSans.ttf]' + 'Руководство пользователя' + '[/font]', markup=True,
                              font_size='14sp', background_color=light_grey)
        support_button = Button(text='[font=OpenSans.ttf]' + 'Поддержка и обратная связь' + '[/font]', markup=True,
                                font_size='14sp', background_color=light_grey)
        share_button = Button(text='[font=OpenSans.ttf]' + 'Поделиться' + '[/font]', markup=True, font_size='14sp',
                              background_color=light_grey)

        layout_v = BoxLayout(orientation='vertical')
        layout_v.add_widget(text_0)
        layout_v.add_widget(text_1)
        layout_v.add_widget(notif_button)
        layout_v.add_widget(genset_button)
        layout_v.add_widget(timerset_button)
        layout_v.add_widget(text_2)
        layout_v.add_widget(icon_button)
        layout_v.add_widget(theme_button)
        layout_v.add_widget(sound_button)
        layout_v.add_widget(text_3)
        layout_v.add_widget(news_button)
        layout_v.add_widget(guide_button)
        layout_v.add_widget(support_button)
        layout_v.add_widget(share_button)

        back = ScrButton(self, text='назад', goal='main', background_color='red', size_hint=(0.4, 1),
                         pos_hint={'center_x': 0.5})
        layout_v.add_widget(back)

        # test_thing = TestBottomBar()
        # layout_v.add_widget(test_thing)

        self.add_widget(layout_v)

        panel_backgroud = BottomPanelBackground_settings()
        panel_backgroud_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.125), pos_hint={'center_x': 0.5})
        panel_backgroud_layout.add_widget(panel_backgroud)

        self.add_widget(panel_backgroud_layout)

        panel_foreground_layout = FloatLayout()
        panel_foreground_layout_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.125),
                                                pos_hint={'center_x': 0.5, 'center_y': 0.06})
        timer_button = Button(background_color=(0, 0, 0, 0))
        timer_button.on_press = self.go_timer
        statistics_button = Button(background_color=(0, 0, 0, 0))
        statistics_button.on_press = self.go_stats
        home_button = Button(size_hint=(1, 1.2), background_color=(0, 0, 0, 0))
        home_button.on_press = self.go_main
        profile_button = Button(background_color=(0, 0, 0, 0))
        profile_button.on_press = self.go_profile
        settings_button = Button(background_color=(0, 0, 0, 0))
        settings_button.on_press = self.go_settings
        panel_foreground_layout_box.add_widget(timer_button)
        panel_foreground_layout_box.add_widget(statistics_button)
        panel_foreground_layout_box.add_widget(home_button)
        panel_foreground_layout_box.add_widget(profile_button)
        panel_foreground_layout_box.add_widget(settings_button)
        panel_foreground_layout.add_widget(panel_foreground_layout_box)

        self.add_widget(panel_foreground_layout)

    def go_timer(self):
        self.manager.current = 'timer'

    def go_stats(self):
        self.manager.current = 'stats'

    def go_main(self):
        self.manager.current = 'main'

    def go_profile(self):
        self.manager.current = 'profile'

    def go_settings(self):
        self.manager.current = 'settings'


'''#секретные разработки нормального перехода между экранами, строго запрщено к просмотру!!!!!##
class Settings(Screen):
    def __init__(self, name='settings'):
        super().__init__(name=name)

        Screen.clearcolor = dark_background_color

        panel_backgroud = BottomPanelBackground()
        panel_backgroud_layout = BoxLayout(orientation='horizontal', size_hint=(1,0.125), pos_hint={'center_x':0.5})
        panel_backgroud_layout.add_widget(panel_backgroud)

        #layout_v = BoxLayout(orientation='vertical')
        layout_v = FloatLayout()
        layout_h = BoxLayout(orientation='horizontal')

        timer_screen_layout = FloatLayout()
        #timer_screen_text = Label(text='таймер', pos_hint={'center_x':0.5, 'center_y':1.5})
        #timer_screen_layout.add_widget(timer_screen_text)

        abc = Timer(name='timer')
        timer_screen_layout.add_widget(abc)

        #, content=timer_screen_layout

        tab_panel = TabbedPanel(pos_hint={'center_y':-0.4}, background_color=(0,0,0,0), do_default_tab = False)
        timer_screen = TabbedPanelHeader(text='Таймер')
        statistics_screen = TabbedPanelHeader(text='Статистика', background_color=(0,0,0,0))
        plus_screen = TabbedPanelHeader(text='Добавить')
        account_screen = TabbedPanelHeader(text='Аккаунт')
        settings_screen = TabbedPanelHeader(text='Настройки')

        #Как менять их ширину? 

        tab_panel.add_widget(timer_screen)
        tab_panel.add_widget(statistics_screen)
        tab_panel.add_widget(plus_screen)
        tab_panel.add_widget(account_screen)
        tab_panel.add_widget(settings_screen)


        layout_h.add_widget(tab_panel)
        #layout_h.add_widget(statistics_screen)
        #layout_h.add_widget(plus_screen)
        #layout_h.add_widget(account_screen)
        #layout_h.add_widget(settings_screen)

        layout_v.add_widget(layout_h)


        #back = ScrButton(self, text='назад', goal='main', background_color='red', size_hint=(0.4,1), pos_hint={'center_x':0.5})
        #layout_v.add_widget(back)


        self.add_widget(panel_backgroud_layout)
        #self.add_widget(layout_v)
'''
'''
    def next(self):
        check_age = check_int(self.input1_2.text)
        if check_age == False or check_age < 7:
            check_age = 0
            self.input1_2.text = str(check_age)
        else:
            self.manager.current = 'second'
            global name1 
            name1 = self.input1_1.text
            global age
            age = self.input1_2.text
'''


####################################################################################################################################################

class MyApp(App):
    def build(self):
        self.sm = ScreenManager(transition=NoTransition())
        # self.sm.add_widget(FirstScreen(name='first'))
        # self.sm.add_widget(SignIn(name='signin'))
        # self.sm.add_widget(LogIn(name='login'))
        # self.sm.add_widget(Reset_Password(name='password_reset'))
        self.main = Main(name='main')
        self.sm.add_widget(self.main)
        self.sm.add_widget(CreateProject(main=self.main, name='createproject'))
        self.sm.add_widget(Timer(name='timer'))
        self.sm.add_widget(Statistics(name='stats'))
        # self.sm.add_widget(Statistics_norm(name='stats_norm'))
        self.sm.add_widget(Profile(name='profile'))
        self.sm.add_widget(Settings_1(name='settings'))

        return self.sm

    def add_widget_at_app(self, screen_name):
        self.sm.add_widget(screen_name)

        return self.sm


app = MyApp()
app.run()