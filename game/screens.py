import kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.app import App
import random

from game.widget import GameWidget
from game.config import CARD_UPGRADES

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)

        # Button zum Öffnen des Skill-Trees
        skill_tree_button = Button(text="Skill-Tree", size_hint=(None, None), size=(150, 50), pos=(10, 10))
        skill_tree_button.bind(on_press=self.open_skill_tree)
        self.add_widget(skill_tree_button)

    def open_skill_tree(self, instance):
        App.get_running_app().screen_manager.current = 'skill_tree'

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

from game.skill_tree_data import SKILL_TREE_DATA

class SkillTreeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Button zum Zurückkehren zum Spiel
        back_button = Button(text="Zurück", size_hint=(None, None), size=(150, 50), pos=(10, 10))
        back_button.bind(on_press=self.back_to_game)
        self.layout.add_widget(back_button)

    def on_enter(self):
        self.populate_skill_tree()

    def populate_skill_tree(self):
        self.layout.canvas.before.clear()
        self.layout.clear_widgets()
        app = App.get_running_app()

        # Manuelle Positionierung für ein einfaches Layout
        node_positions = {
            'start_node': (100, 300),
            'strength_1': (200, 400),
            'strength_2': (300, 400),
            'dexterity_1': (200, 200),
            'dexterity_2': (300, 200),
            'art_of_the_gladiator': (400, 300),
            'life_1': (400, 450),
        }

        for node_id, node_data in SKILL_TREE_DATA.items():
            is_unlocked = node_id in app.player_data.unlocked_nodes

            # Farbe basierend auf dem Status des Knotens
            bg_color = (0.2, 0.8, 0.2, 1) if is_unlocked else (0.5, 0.5, 0.5, 1)

            node_button = Button(
                text=node_data['name'],
                size_hint=(None, None),
                size=(150, 50),
                pos=node_positions.get(node_id, (0, 0)),
                background_color=bg_color
            )
            node_button.bind(on_press=lambda instance, n_id=node_id: self.unlock_node(n_id))
            self.layout.add_widget(node_button)

        # Zurück-Button und Skill-Punkt-Anzeige hinzufügen, nachdem die Knoten hinzugefügt wurden
        back_button = Button(text="Zurück", size_hint=(None, None), size=(150, 50), pos=(10, 10))
        back_button.bind(on_press=self.back_to_game)
        self.layout.add_widget(back_button)

        self.skill_point_label = Label(
            text=f"Skill-Punkte: {app.player_data.skill_points}",
            size_hint=(None, None),
            size=(200, 50),
            pos=(self.width - 210, 10)
        )
        self.layout.add_widget(self.skill_point_label)


        with self.layout.canvas.before:
            for node_id, node_data in SKILL_TREE_DATA.items():
                for connection_id in node_data.get('connections', []):
                    # Sicherstellen, dass die Verbindung existiert und Duplikate vermieden werden
                    if connection_id in SKILL_TREE_DATA and connection_id > node_id:
                        start_pos = node_positions.get(node_id)
                        end_pos = node_positions.get(connection_id)

                        if start_pos and end_pos:
                            is_active = node_id in app.player_data.unlocked_nodes and \
                                        connection_id in app.player_data.unlocked_nodes

                            color = (0.8, 0.8, 0.2, 1) if is_active else (0.3, 0.3, 0.3, 1)
                            Color(*color)
                            Line(points=[start_pos[0] + 75, start_pos[1] + 25, end_pos[0] + 75, end_pos[1] + 25], width=2)


    def unlock_node(self, node_id):
        app = App.get_running_app()
        node_data = SKILL_TREE_DATA[node_id]
        cost = node_data.get('cost', 1)

        # 1. Ist der Knoten bereits freigeschaltet?
        if node_id in app.player_data.unlocked_nodes:
            print(f"Knoten '{node_id}' ist bereits freigeschaltet.")
            return

        # 2. Genügend Skill-Punkte?
        if app.player_data.skill_points < cost:
            print("Nicht genügend Skill-Punkte.")
            return

        # 3. Ist eine Verbindung zu einem freigeschalteten Knoten vorhanden?
        # Der Startknoten ist eine Ausnahme.
        # 3. Ist eine Verbindung zu einem freigeschalteten Knoten vorhanden?
        is_connected = (node_id == 'start_node') # Der Startknoten benötigt keine Verbindung.
        if not is_connected:
            # Durchsuche alle Knoten, um zu sehen, ob einer von ihnen mit dem aktuellen verbunden ist
            for other_node_id, other_node_data in SKILL_TREE_DATA.items():
                # Ist der andere Knoten freigeschaltet?
                if other_node_id in app.player_data.unlocked_nodes:
                    # Führt eine Verbindung vom freigeschalteten Knoten zum Zielknoten?
                    if node_id in other_node_data.get('connections', []):
                        is_connected = True
                        break

            # Überprüfe auch die eigenen Verbindungen des Zielknotens, falls noch keine Verbindung gefunden wurde
            if not is_connected:
                for connected_id in node_data.get('connections', []):
                    if connected_id in app.player_data.unlocked_nodes:
                        is_connected = True
                        break

        if not is_connected:
            print("Knoten ist nicht mit einem freigeschalteten Knoten verbunden.")
            return

        # Alle Prüfungen bestanden -> Knoten freischalten
        print(f"Schalte Knoten '{node_id}' frei...")
        app.player_data.skill_points -= cost
        app.player_data.unlocked_nodes.add(node_id)
        app.player_data.save_data()

        # Stats neu berechnen, um Boni anzuwenden
        app.game_widget.player.calculate_stats()

        # UI aktualisieren
        self.populate_skill_tree()


    def back_to_game(self, instance):
        App.get_running_app().screen_manager.current = 'game'