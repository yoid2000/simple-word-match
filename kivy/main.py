from kivy.config import Config
Config.set('graphics', 'width', '400')   # Set to your phone's width in pixels
Config.set('graphics', 'height', '800')  # Set to your phone's height in pixels
Config.set('graphics', 'resizable', '0') # Optional: make window non-resizable

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.actionbar import ActionBar, ActionButton
from kivy.uix.actionbar import ActionView, ActionPrevious
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.clock import Clock
import os
import json
import random
from word_manager import WordManager


class WordMatchScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.word_manager = WordManager(num_words=10)
        self.english_buttons = []
        self.german_buttons = []
        self.feedback_popup = None
        self.first_click_column = None  # 'english' or 'german' or None
        self.first_click_index = None
        self.first_click_type = None  # 'single' or 'double'
        self.first_click_highlight = None  # (column, idx, color)
        self.build_ui()
        self.load_words()

    def select_english(self, idx, click_type='single'):
        if self.english_words[idx]['color'] not in ['black', 'red', 'lightgrey', 'lightblue']:
            return
        import sys
        print(f"INFO: select_english called: idx={idx}, click_type={click_type}", file=sys.stdout)
        if self.first_click_column is None or self.first_click_column == 'english':
            print(f"INFO: FIRST CLICK (english, idx={idx}, type={click_type})", file=sys.stdout)
            self.first_click_column = 'english'
            self.first_click_index = idx
            self.first_click_type = click_type
            # Update internal state: set clicked word to green/blue, reset only green in both columns
            for i, word in enumerate(self.english_words):
                if i == idx:
                    word['color'] = 'lightblue' if click_type == 'double' else 'green'
                elif word['color'] == 'green':
                    word['color'] = 'black'
            for i, word in enumerate(self.german_words):
                if word['color'] == 'green':
                    word['color'] = 'black'
            self.print_internal_state()
            self.refresh_display()
        else:
            # This is a second click (first click was german)
            if self.first_click_index is not None:
                click_type = self.first_click_type if self.first_click_type is not None else 'single'
                print(f"INFO: SECOND CLICK (english, idx={idx}, type={click_type})", file=sys.stdout)
                # Determine if match is correct
                correct = self.word_manager.english_order[idx] == self.word_manager.german_order[self.first_click_index]
                print(f"INFO: MATCH OUTCOME: {'CORRECT' if correct else 'INCORRECT'}", file=sys.stdout)
                self.english_words, self.german_words = self.word_manager.get_words(
                    english_index=idx, german_index=self.first_click_index, click_type=click_type)
            self.first_click_column = None
            self.first_click_index = None
            self.first_click_type = None
            self.print_internal_state()
            self.refresh_display()

    def select_german(self, idx, click_type='single'):
        if self.german_words[idx]['color'] not in ['black', 'red', 'lightgrey', 'lightblue']:
            return
        import sys
        print(f"INFO: select_german called: idx={idx}, click_type={click_type}", file=sys.stdout)
        if self.first_click_column is None or self.first_click_column == 'german':
            print(f"INFO: FIRST CLICK (german, idx={idx}, type={click_type})", file=sys.stdout)
            self.first_click_column = 'german'
            self.first_click_index = idx
            self.first_click_type = click_type
            # Update internal state: set clicked word to green/blue, reset only green in both columns
            for i, word in enumerate(self.german_words):
                if i == idx:
                    word['color'] = 'lightblue' if click_type == 'double' else 'green'
                elif word['color'] == 'green':
                    word['color'] = 'black'
            for i, word in enumerate(self.english_words):
                if word['color'] == 'green':
                    word['color'] = 'black'
            self.print_internal_state()
            self.refresh_display()
        else:
            # This is a second click (first click was english)
            if self.first_click_index is not None:
                click_type = self.first_click_type if self.first_click_type is not None else 'single'
                print(f"INFO: SECOND CLICK (german, idx={idx}, type={click_type})", file=sys.stdout)
                # Determine if match is correct
                correct = self.word_manager.english_order[self.first_click_index] == self.word_manager.german_order[idx]
                print(f"INFO: MATCH OUTCOME: {'CORRECT' if correct else 'INCORRECT'}", file=sys.stdout)
                self.english_words, self.german_words = self.word_manager.get_words(
                    english_index=self.first_click_index, german_index=idx, click_type=click_type)
            self.first_click_column = None
            self.first_click_index = None
            self.first_click_type = None
            self.print_internal_state()
            self.refresh_display()
    def print_internal_state(self):
        import sys
        print("INFO: Internal English State:", [(w['word'], w['color']) for w in self.english_words], file=sys.stdout)
        print("INFO: Internal German State:", [(w['word'], w['color']) for w in self.german_words], file=sys.stdout)
        # Print frequent words state
        if hasattr(self.word_manager, 'frequent_words'):
            print("INFO: Frequent Words State:", self.word_manager.frequent_words, file=sys.stdout)

    # handle_pair removed; logic now in select_english/select_german

    def refresh_display(self):
        self.english_col.clear_widgets()
        self.german_col.clear_widgets()
        self.english_buttons = []
        self.german_buttons = []
        button_spacing = 8  # tight spacing
        for i, word in enumerate(self.english_words):
            btn = DoubleTapButton(
                text=word['word'],
                background_color=self.get_color(word['color']),
                size_hint_y=None,
                halign='center',
                valign='middle',
                padding=[2, 0],
                font_size=80
            )
            # Enable wrap-around
            btn.text_size = (btn.width, None)
            btn.bind(
                width=lambda instance, value: setattr(instance, 'text_size', (value, None))
            )
            btn.bind(
                texture_size=lambda instance, value: setattr(instance, 'height', value[1] + 2)
            )
            btn.single_tap_callback = lambda idx=i: self.select_english(idx, 'single')
            btn.double_tap_callback = lambda idx=i: self.on_english_double_tap(idx)
            self.english_col.add_widget(btn)
            self.english_buttons.append(btn)
        for i, word in enumerate(self.german_words):
            btn = DoubleTapButton(
                text=word['word'],
                background_color=self.get_color(word['color']),
                size_hint_y=None,
                halign='center',
                valign='middle',
                padding=[2, 0],
                font_size=80
            )
            btn.text_size = (btn.width, None)
            btn.bind(
                width=lambda instance, value: setattr(instance, 'text_size', (value, None))
            )
            btn.bind(
                texture_size=lambda instance, value: setattr(instance, 'height', value[1] + 2)
            )
            btn.single_tap_callback = lambda idx=i: self.select_german(idx, 'single')
            btn.double_tap_callback = lambda idx=i: self.on_german_double_tap(idx)
            self.german_col.add_widget(btn)
            self.german_buttons.append(btn)
        self.english_col.spacing = button_spacing
        self.german_col.spacing = button_spacing

    def get_color(self, color_name):
        colors = {
            'black': [0.6,0.6,0.6,1],
            'red': [1,0,0,1],
            #'lightgrey': [0.99,0.99,0.99,1.0],  # even lighter grey
            'lightgrey': [1,1,1,1],  # even lighter grey
            'lightblue': [0.5,0.7,1,1],
            'yellow': [1,1,0,1],
            'green': [0.3,1,0.3,1],  # brighter green
        }
        return colors.get(color_name, [0,0,0,1])
    # __init__ moved above

    def build_ui(self):
        # Main grid (no title)
        self.grid = GridLayout(cols=2, spacing=10, size_hint=(1, 0.9))

        # English column in a ScrollView
        self.english_col = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.english_col.bind(minimum_height=self.english_col.setter('height'))
        english_scroll = ScrollView(size_hint=(1, 1))
        english_scroll.add_widget(self.english_col)

        # German column in a ScrollView
        self.german_col = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.german_col.bind(minimum_height=self.german_col.setter('height'))
        german_scroll = ScrollView(size_hint=(1, 1))
        german_scroll.add_widget(self.german_col)

        self.grid.add_widget(english_scroll)
        self.grid.add_widget(german_scroll)
        self.add_widget(self.grid)


    def on_english_double_tap(self, idx):
        self.select_english(idx, 'double')

    def on_german_double_tap(self, idx):
        self.select_german(idx, 'double')

    def load_words(self):
        self.english_words, self.german_words = self.word_manager.get_words()
        self.first_click_column = None
        self.first_click_index = None
        self.first_click_type = None
        # Do not reset colors here; only after a round or match
        self.refresh_display()
class DoubleTapButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_touch_time = 0
        self.double_tap_time = 0.2  # seconds (slightly reduced for snappier feel)
        self.single_tap_callback = lambda: None
        self.double_tap_callback = lambda: None
        self._single_tap_pending = False

    def on_release(self):
        import time
        now = time.time()
        import sys
        if self._single_tap_pending and (now - self.last_touch_time) < self.double_tap_time:
            # This is a double tap
            print(f"INFO: DOUBLE TAP detected on button '{self.text}'", file=sys.stdout)
            self._single_tap_pending = False
            if self.double_tap_callback:
                self.double_tap_callback()
        else:
            # Schedule single tap, but wait to see if a double tap comes in
            self._single_tap_pending = True
            self.last_touch_time = now
            from kivy.clock import Clock
            Clock.schedule_once(self._do_single_tap, self.double_tap_time)
        return super().on_release()

    def _do_single_tap(self, dt):
        import time
        import sys
        if self._single_tap_pending:
            print(f"INFO: SINGLE TAP detected on button '{self.text}'", file=sys.stdout)
            if self.single_tap_callback:
                self.single_tap_callback()
            self._single_tap_pending = False




class SimpleWordMatchApp(App):
    def build(self):
        return WordMatchScreen()

if __name__ == '__main__':
    SimpleWordMatchApp().run()
