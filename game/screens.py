import kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
import random

from game.widget import GameWidget
from game.config import CARD_UPGRADES

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)

class CardSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        self.add_widget(self.layout)

    def on_enter(self):
        """
        Wird aufgerufen, wenn der Bildschirm angezeigt wird. Füllt den Bildschirm mit neuen Karten.
        """
        self.populate_cards()

    def populate_cards(self):
        """
        Erstellt und zeigt drei zufällige Upgrade-Karten als Buttons an.
        """
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text="Level Up! Wähle eine Verbesserung:", font_size='30sp', size_hint_y=0.2))

        selected_cards = random.sample(CARD_UPGRADES, 3)

        for card_data in selected_cards:
            btn = Button(text=card_data['text'], font_size='20sp', size_hint_y=0.25)
            btn.bind(on_press=lambda instance, data=card_data: self.on_card_selection(data))
            self.layout.add_widget(btn)

    def on_card_selection(self, card_data):
        """
        Wird aufgerufen, wenn eine Karte ausgewählt wird. Wendet den Bonus an und kehrt zum Spiel zurück.
        """
        print(f"Karte ausgewählt: {card_data['text']}")
        # Hier wird die Logik zum Anwenden des Upgrades hinzugefügt
        app = App.get_running_app()
        app.apply_upgrade(card_data)

        # Zurück zum Spiel
        app.screen_manager.current = 'game'