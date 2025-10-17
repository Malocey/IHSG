import kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from game.widget import GameWidget

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)

class CardSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Level Up! Wähle eine Karte.", font_size='30sp'))