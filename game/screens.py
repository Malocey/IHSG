import kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle
from kivy.app import App
from kivy.core.window import Window
import random

from game.widget import GameWidget
from game.config import CARD_UPGRADES

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)

        # Button zum Öffnen des Skill-Trees
        skill_tree_button = Button(text="Skill-Tree", size_hint=(None, None), size=(150, 50), pos=(170, 10))
        skill_tree_button.bind(on_press=self.open_skill_tree)
        self.add_widget(skill_tree_button)

        # Button zum Betreten der Stadt
        city_button = Button(text="Stadt", size_hint=(None, None), size=(150, 50), pos=(10, 10))
        city_button.bind(on_press=self.go_to_city)
        self.add_widget(city_button)

    def open_skill_tree(self, instance):
        App.get_running_app().screen_manager.current = 'skill_tree'

    def go_to_city(self, instance):
        App.get_running_app().screen_manager.current = 'city'

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

class TooltipLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.font_size = '14sp'
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 0.9)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class MouseControllable:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        if self.collide_point(*self.to_widget(*pos)):
            if not self.hovered:
                self.on_enter()
                self.hovered = True
        elif self.hovered:
            self.on_leave()
            self.hovered = False

    def on_enter(self):
        pass

    def on_leave(self):
        pass

class SkillNodeButton(MouseControllable, Button):
    hovered = False
    def __init__(self, node_data, **kwargs):
        super().__init__(**kwargs)
        self.node_data = node_data

    def on_enter(self):
        App.get_running_app().root.get_screen('skill_tree').show_tooltip(self.node_data, self.to_window(self.center_x, self.top))

    def on_leave(self):
        App.get_running_app().root.get_screen('skill_tree').hide_tooltip()

class SkillTreeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root_layout = FloatLayout()

        self.scatter_layout = ScatterLayout(
            do_rotation=False, do_scale=True, do_translation=True,
            size_hint=(None, None), size=(3000, 2000)
        )

        self.skill_tree_layout = FloatLayout()
        self.scatter_layout.add_widget(self.skill_tree_layout)

        self.root_layout.add_widget(self.scatter_layout)
        self.add_widget(self.root_layout)

        back_button = Button(text="Zurück", size_hint=(None, None), size=(150, 50), pos=(10, 10))
        back_button.bind(on_press=self.back_to_game)
        self.root_layout.add_widget(back_button)

        app = App.get_running_app()
        self.skill_point_label = Label(
            text=f"Skill-Punkte: {app.player_data.skill_points if app else 0}",
            size_hint=(None, None), size=(200, 50)
        )
        self.root_layout.add_widget(self.skill_point_label)
        self.bind(size=self._update_skill_point_label_pos)

        self.tooltip = TooltipLabel(text='')
        self.tooltip.opacity = 0

    def _update_skill_point_label_pos(self, instance, value):
        self.skill_point_label.pos = (self.width - 210, 10)

    def on_enter(self):
        self.populate_skill_tree()
        app = App.get_running_app()
        self.skill_point_label.text = f"Skill-Punkte: {app.player_data.skill_points}"

    def populate_skill_tree(self):
        self.skill_tree_layout.canvas.before.clear()
        self.skill_tree_layout.clear_widgets()
        app = App.get_running_app()

        node_positions = {
            # Center
            'start_node': (1500, 1000),
            # Strength Path (Top-Left)
            'strength_1': (1350, 1150), 'strength_2': (1200, 1250),
            'armor_1': (1050, 1350), 'elemental_resistance_1': (900, 1450),
            'shield_mastery': (750, 1550),
            # Dexterity Path (Top-Right)
            'dexterity_1': (1650, 1150), 'dexterity_2': (1800, 1250),
            'crit_chance_1': (1950, 1350), 'crit_damage_1': (2100, 1450),
            'lethal_precision': (2250, 1550),
            # Intelligence Path (Bottom-Center)
            'intelligence_1': (1500, 850), 'intelligence_2': (1500, 700),
            'mana_1': (1500, 550), 'arcane_potency': (1500, 400),
            # Life Path (Left)
            'life_1': (1200, 1000), 'life_2': (1000, 1000), 'vitality_1': (800, 1000),
            # Notable Connections
            'art_of_the_gladiator': (1500, 1400),
            # Keystone
            'keystone_bulwark': (500, 1250),
            # Loose nodes
            'attack_speed_1': (1650, 1450),
            'movement_speed_1': (1800, 1100),
            'mana_regen_1': (1650, 650),
            'evasion_1': (2400, 1500),
            'area_of_effect_1': (1350, 350),
            'all_attributes_1': (1500, 1550),
        }

        node_widgets = {}

        for node_id, node_data in SKILL_TREE_DATA.items():
            is_unlocked = node_id in app.player_data.unlocked_nodes
            node_type = node_data.get('node_type', 'minor')
            size, color = self.get_node_style(node_type, is_unlocked)

            pos = node_positions.get(node_id, (0, 0))
            node_button = SkillNodeButton(
                node_data=node_data,
                text=node_data['name'],
                size_hint=(None, None),
                size=size,
                pos=pos,
                background_normal='',
                background_color=color
            )
            node_button.bind(on_press=lambda instance, n_id=node_id: self.unlock_node(n_id))
            self.skill_tree_layout.add_widget(node_button)
            node_widgets[node_id] = node_button

        with self.skill_tree_layout.canvas.before:
            for node_id, node_data in SKILL_TREE_DATA.items():
                start_widget = node_widgets.get(node_id)
                for connection_id in node_data.get('connections', []):
                    end_widget = node_widgets.get(connection_id)

                    if start_widget and end_widget:
                        is_active = node_id in app.player_data.unlocked_nodes and \
                                    connection_id in app.player_data.unlocked_nodes
                        color = (0.8, 0.8, 0.2, 1) if is_active else (0.3, 0.3, 0.3, 1)
                        Color(*color)
                        Line(points=[start_widget.center_x, start_widget.center_y, end_widget.center_x, end_widget.center_y], width=2)

    def show_tooltip(self, node_data, pos):
        self.tooltip.text = f"{node_data['name']}\n\n{node_data['description']}\nKosten: {node_data.get('cost', 1)}"
        self.tooltip.texture_update()
        self.tooltip.size = self.tooltip.texture_size
        self.tooltip.pos = (pos[0] - self.tooltip.width / 2, pos[1] + 10)

        if self.tooltip not in self.root_layout.children:
            self.root_layout.add_widget(self.tooltip)
        self.tooltip.opacity = 1

    def hide_tooltip(self):
        self.tooltip.opacity = 0
        if self.tooltip in self.root_layout.children:
            self.root_layout.remove_widget(self.tooltip)

    def get_node_style(self, node_type, is_unlocked):
        if node_type == 'keystone':
            size = (140, 140)
            color = (1.0, 0.2, 0.2, 1) if is_unlocked else (0.6, 0.1, 0.1, 1)
        elif node_type == 'start':
            size = (120, 120)
            color = (0.7, 0.5, 0.9, 1) if is_unlocked else (0.4, 0.3, 0.5, 1)
        elif node_type == 'notable':
            size = (100, 100)
            color = (0.9, 0.7, 0.2, 1) if is_unlocked else (0.5, 0.4, 0.1, 1)
        else:  # minor
            size = (60, 60)
            color = (0.2, 0.8, 0.2, 1) if is_unlocked else (0.5, 0.5, 0.5, 1)
        return size, color


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
        self.skill_point_label.text = f"Skill-Punkte: {app.player_data.skill_points}"


    def back_to_game(self, instance):
        App.get_running_app().screen_manager.current = 'game'

    def go_to_shop(self, instance):
        App.get_running_app().screen_manager.current = 'shop'


class ShopScreen(Screen):
    """
    Der Shop-Bildschirm für permanente Upgrades.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        title = Label(text="Händler", font_size='30sp', size_hint_y=None, height=50)
        self.gold_label = Label(text="", font_size='20sp', size_hint_y=None, height=40)

        self.layout.add_widget(title)
        self.layout.add_widget(self.gold_label)

        self.upgrades_layout = BoxLayout(orientation='vertical', spacing=15)
        self.layout.add_widget(self.upgrades_layout)

        back_button = Button(text="Zurück zur Stadt", size_hint_y=None, height=50)
        back_button.bind(on_press=self.back_to_city)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def on_enter(self):
        """Wird aufgerufen, wenn der Bildschirm betreten wird, um die UI zu aktualisieren."""
        self.update_ui()

    def update_ui(self):
        """Aktualisiert die gesamte Shop-UI mit aktuellen Daten."""
        app = App.get_running_app()
        self.gold_label.text = f"Dein Gold: {app.player_data.gold}"

        self.upgrades_layout.clear_widgets()

        from game.config import SHOP_UPGRADES
        for upgrade_id, upgrade_data in SHOP_UPGRADES.items():
            current_level = app.player_data.shop_upgrades.get(upgrade_id, 0)

            # Preisnachlass anwenden
            base_cost = upgrade_data['cost_formula'](current_level)
            price_reduction = app.shop_price_percent
            cost = int(base_cost * (1 - price_reduction))

            upgrade_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)

            info_text = f"{upgrade_data['name']} (Level {current_level})\n{upgrade_data['description']}"
            info_label = Label(text=info_text, halign='left', valign='middle')
            info_label.bind(size=info_label.setter('text_size'))

            buy_button = Button(text=f"Kaufen ({cost} G)", size_hint_x=0.4)
            buy_button.bind(on_press=lambda instance, u_id=upgrade_id: self.buy_upgrade(u_id))

            if app.player_data.gold < cost:
                buy_button.disabled = True

            max_level = upgrade_data.get('max_level')
            if max_level is not None and current_level >= max_level:
                buy_button.text = "Max Level"
                buy_button.disabled = True

            upgrade_box.add_widget(info_label)
            upgrade_box.add_widget(buy_button)
            self.upgrades_layout.add_widget(upgrade_box)

    def buy_upgrade(self, upgrade_id):
        """Führt die Logik zum Kaufen eines Upgrades aus."""
        app = App.get_running_app()
        from game.config import SHOP_UPGRADES

        upgrade_data = SHOP_UPGRADES[upgrade_id]
        current_level = app.player_data.shop_upgrades.get(upgrade_id, 0)

        # Kosten mit Preisnachlass berechnen
        base_cost = upgrade_data['cost_formula'](current_level)
        price_reduction = app.shop_price_percent
        cost = int(base_cost * (1 - price_reduction))

        if app.player_data.gold >= cost:
            app.player_data.gold -= cost
            app.player_data.shop_upgrades[upgrade_id] = current_level + 1
            app.player_data.save_data()

            # Wichtig: Stats neu berechnen, da sich der Preisnachlass ändern könnte
            if hasattr(app, 'calculate_stats'):
                app.calculate_stats()

            self.update_ui() # UI nach dem Kauf aktualisieren
        else:
            print("Nicht genug Gold!")

    def back_to_city(self, instance):
        App.get_running_app().screen_manager.current = 'city'

class CityScreen(Screen):
    """
    Der Stadt-Bildschirm, der als zentraler Hub für Meta-Gameplay-Features dient.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Platzhalter-Titel
        title = Label(text="Willkommen in der Stadt", font_size='30sp', size_hint=(None, None), size=(400, 50))
        title.bind(size=self._update_title_pos)
        self.bind(size=lambda *args: self._update_title_pos(title, self.size))
        layout.add_widget(title)

        # Händler-Button
        merchant_button = Button(text="Händler", size_hint=(None, None), size=(200, 80), pos=(100, 250))
        merchant_button.bind(on_press=self.go_to_shop)
        layout.add_widget(merchant_button)

        # Schmied-Button (vorerst ohne Funktion)
        blacksmith_button = Button(text="Schmied", size_hint=(None, None), size=(200, 80), pos=(self.width - 300, 250))
        layout.add_widget(blacksmith_button)

        # Button zum Zurückkehren zum Spiel
        back_button = Button(text="Zurück zum Kampf!", size_hint=(None, None), size=(200, 50), pos=(10, 10))
        back_button.bind(on_press=self.back_to_game)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def _update_title_pos(self, instance, size):
        instance.pos = (size[0] / 2 - instance.width / 2, size[1] - 100)

    def back_to_game(self, instance):
        App.get_running_app().screen_manager.current = 'game'