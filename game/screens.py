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
import shutil
import os

from game.widget import GameWidget
from game.config import CARD_UPGRADES
from game.skill_tree_data import SKILL_TREE_DATA
from game.item_data import ITEM_DATA, EQUIPMENT_SLOTS

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
        self.populate_cards()

    def populate_cards(self):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text="Level Up! Wähle eine Verbesserung:", font_size='30sp', size_hint_y=0.2))
        selected_cards = random.sample(CARD_UPGRADES, 3)
        for card_data in selected_cards:
            btn = Button(text=card_data['text'], font_size='20sp', size_hint_y=0.25)
            btn.bind(on_press=lambda instance, data=card_data: self.on_card_selection(data))
            self.layout.add_widget(btn)

    def on_card_selection(self, card_data):
        print(f"Karte ausgewählt: {card_data['text']}")
        app = App.get_running_app()
        app.apply_upgrade(card_data)
        app.screen_manager.current = 'game'

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
        self.scatter_layout = ScatterLayout(do_rotation=False, do_scale=True, do_translation=True, size_hint=(None, None), size=(3000, 2000))
        self.skill_tree_layout = FloatLayout()
        self.scatter_layout.add_widget(self.skill_tree_layout)
        self.root_layout.add_widget(self.scatter_layout)
        self.add_widget(self.root_layout)
        back_button = Button(text="Zurück", size_hint=(None, None), size=(150, 50), pos=(10, 10))
        back_button.bind(on_press=self.back_to_game)
        self.root_layout.add_widget(back_button)
        app = App.get_running_app()
        self.skill_point_label = Label(text=f"Skill-Punkte: {app.player_data.skill_points if app else 0}", size_hint=(None, None), size=(200, 50))
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
            'start_node': (1500, 1000), 'strength_1': (1350, 1150), 'strength_2': (1200, 1250),
            'armor_1': (1050, 1350), 'elemental_resistance_1': (900, 1450), 'shield_mastery': (750, 1550),
            'dexterity_1': (1650, 1150), 'dexterity_2': (1800, 1250), 'crit_chance_1': (1950, 1350),
            'crit_damage_1': (2100, 1450), 'lethal_precision': (2250, 1550), 'intelligence_1': (1500, 850),
            'intelligence_2': (1500, 700), 'mana_1': (1500, 550), 'arcane_potency': (1500, 400),
            'life_1': (1200, 1000), 'life_2': (1000, 1000), 'vitality_1': (800, 1000),
            'art_of_the_gladiator': (1500, 1400), 'keystone_bulwark': (500, 1250),
            'attack_speed_1': (1650, 1450), 'movement_speed_1': (1800, 1100), 'mana_regen_1': (1650, 650),
            'evasion_1': (2400, 1500), 'area_of_effect_1': (1350, 350), 'all_attributes_1': (1500, 1550),
        }
        node_widgets = {}
        for node_id, node_data in SKILL_TREE_DATA.items():
            is_unlocked = node_id in app.player_data.unlocked_nodes
            node_type = node_data.get('node_type', 'minor')
            size, color = self.get_node_style(node_type, is_unlocked)
            pos = node_positions.get(node_id, (0, 0))
            node_button = SkillNodeButton(node_data=node_data, text=node_data['name'], size_hint=(None, None), size=size, pos=pos, background_normal='', background_color=color)
            node_button.bind(on_press=lambda instance, n_id=node_id: self.unlock_node(n_id))
            self.skill_tree_layout.add_widget(node_button)
            node_widgets[node_id] = node_button
        with self.skill_tree_layout.canvas.before:
            for node_id, node_data in SKILL_TREE_DATA.items():
                start_widget = node_widgets.get(node_id)
                for connection_id in node_data.get('connections', []):
                    end_widget = node_widgets.get(connection_id)
                    if start_widget and end_widget:
                        is_active = node_id in app.player_data.unlocked_nodes and connection_id in app.player_data.unlocked_nodes
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
        else:
            size = (60, 60)
            color = (0.2, 0.8, 0.2, 1) if is_unlocked else (0.5, 0.5, 0.5, 1)
        return size, color

    def unlock_node(self, node_id):
        app = App.get_running_app()
        node_data = SKILL_TREE_DATA[node_id]
        cost = node_data.get('cost', 1)
        if node_id in app.player_data.unlocked_nodes:
            print(f"Knoten '{node_id}' ist bereits freigeschaltet.")
            return
        if app.player_data.skill_points < cost:
            print("Nicht genügend Skill-Punkte.")
            return
        is_connected = (node_id == 'start_node')
        if not is_connected:
            for other_node_id, other_node_data in SKILL_TREE_DATA.items():
                if other_node_id in app.player_data.unlocked_nodes:
                    if node_id in other_node_data.get('connections', []):
                        is_connected = True
                        break
            if not is_connected:
                for connected_id in node_data.get('connections', []):
                    if connected_id in app.player_data.unlocked_nodes:
                        is_connected = True
                        break
        if not is_connected:
            print("Knoten ist nicht mit einem freigeschalteten Knoten verbunden.")
            return
        print(f"Schalte Knoten '{node_id}' frei...")
        app.player_data.skill_points -= cost
        app.player_data.unlocked_nodes.add(node_id)
        app.player_data.save_data()
        app.game_widget.player.calculate_stats()
        self.populate_skill_tree()
        self.skill_point_label.text = f"Skill-Punkte: {app.player_data.skill_points}"

    def back_to_game(self, instance):
        App.get_running_app().screen_manager.current = 'game'

class CityScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        title = Label(text="Willkommen in der Stadt", font_size='30sp', size_hint=(None, None), size=(400, 50))
        title.bind(size=self._update_title_pos)
        self.bind(size=lambda *args: self._update_title_pos(title, self.size))
        layout.add_widget(title)
        merchant_button = Button(text="Händler", size_hint=(None, None), size=(200, 80), pos=(100, 250))
        merchant_button.bind(on_press=self.go_to_shop)
        layout.add_widget(merchant_button)
        blacksmith_button = Button(text="Schmied", size_hint=(None, None), size=(200, 80), pos=(self.width - 300, 250))
        layout.add_widget(blacksmith_button)
        equipment_button = Button(text="Ausrüstung", size_hint=(None, None), size=(200, 80), pos=(100, 150))
        equipment_button.bind(on_press=self.go_to_equipment)
        layout.add_widget(equipment_button)
        settings_button = Button(text="Einstellungen", size_hint=(None, None), size=(200, 80), pos=(self.width - 300, 150))
        settings_button.bind(on_press=self.go_to_settings)
        layout.add_widget(settings_button)
        back_button = Button(text="Zurück zum Kampf!", size_hint=(None, None), size=(200, 50), pos=(10, 10))
        back_button.bind(on_press=self.back_to_game)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def _update_title_pos(self, instance, size):
        instance.pos = (size[0] / 2 - instance.width / 2, size[1] - 100)

    def back_to_game(self, instance):
        App.get_running_app().screen_manager.current = 'game'

    def go_to_shop(self, instance):
        App.get_running_app().screen_manager.current = 'shop'

    def go_to_equipment(self, instance):
        App.get_running_app().screen_manager.current = 'equipment'

    def go_to_settings(self, instance):
        App.get_running_app().screen_manager.current = 'settings'

class ShopScreen(Screen):
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
        self.update_ui()

    def update_ui(self):
        app = App.get_running_app()
        self.gold_label.text = f"Dein Gold: {app.player_data.gold}"
        self.upgrades_layout.clear_widgets()
        from game.config import SHOP_UPGRADES
        for upgrade_id, upgrade_data in SHOP_UPGRADES.items():
            current_level = app.player_data.shop_upgrades.get(upgrade_id, 0)
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
        app = App.get_running_app()
        from game.config import SHOP_UPGRADES
        upgrade_data = SHOP_UPGRADES[upgrade_id]
        current_level = app.player_data.shop_upgrades.get(upgrade_id, 0)
        base_cost = upgrade_data['cost_formula'](current_level)
        price_reduction = app.shop_price_percent
        cost = int(base_cost * (1 - price_reduction))
        if app.player_data.gold >= cost:
            app.player_data.gold -= cost
            app.player_data.shop_upgrades[upgrade_id] = current_level + 1
            app.player_data.save_data()
            if hasattr(app, 'calculate_stats'):
                app.calculate_stats()
            self.update_ui()
        else:
            print("Nicht genug Gold!")

    def back_to_city(self, instance):
        App.get_running_app().screen_manager.current = 'city'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        title = Label(text="Einstellungen", font_size='30sp', size_hint_y=0.2)
        self.feedback_label = Label(text="", size_hint_y=0.1)
        export_button = Button(text="Spielstand Exportieren", size_hint_y=0.2)
        export_button.bind(on_press=self.export_save)
        import_button = Button(text="Spielstand Importieren", size_hint_y=0.2)
        import_button.bind(on_press=self.import_save)
        back_button = Button(text="Zurück zur Stadt", size_hint_y=0.15)
        back_button.bind(on_press=self.back_to_city)
        layout.add_widget(title)
        layout.add_widget(export_button)
        layout.add_widget(import_button)
        layout.add_widget(self.feedback_label)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def export_save(self, instance):
        source_path = 'player_save.json'
        export_dir = 'exported_save'
        export_path = os.path.join(export_dir, 'player_save.json')
        if not os.path.exists(source_path):
            self.feedback_label.text = "Fehler: Keine Speicherdatei zum Exportieren gefunden."
            return
        try:
            os.makedirs(export_dir, exist_ok=True)
            shutil.copy(source_path, export_path)
            self.feedback_label.text = f"Erfolg! Spielstand nach '{export_path}' exportiert."
        except Exception as e:
            self.feedback_label.text = f"Fehler beim Exportieren: {e}"

    def import_save(self, instance):
        source_path = os.path.join('exported_save', 'player_save.json')
        dest_path = 'player_save.json'
        if not os.path.exists(source_path):
            self.feedback_label.text = "Fehler: Keine Speicherdatei im 'exported_save'-Ordner gefunden."
            return
        try:
            shutil.copy(source_path, dest_path)
            app = App.get_running_app()
            app.player_data.load_data()
            app.calculate_stats()
            self.feedback_label.text = "Erfolg! Spielstand importiert. Änderungen sind aktiv."
        except Exception as e:
            self.feedback_label.text = f"Fehler beim Importieren: {e}"

    def back_to_city(self, instance):
        App.get_running_app().screen_manager.current = 'city'

class EquipmentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root_layout = BoxLayout(orientation='horizontal', padding=20, spacing=20)
        equipment_panel = BoxLayout(orientation='vertical', size_hint_x=0.4)
        equipment_panel.add_widget(Label(text="Ausrüstung", font_size='24sp', size_hint_y=0.1))
        self.equipment_layout = BoxLayout(orientation='vertical', spacing=10)
        equipment_panel.add_widget(self.equipment_layout)
        inventory_panel = BoxLayout(orientation='vertical', size_hint_x=0.6)
        inventory_panel.add_widget(Label(text="Inventar", font_size='24sp', size_hint_y=0.1))
        self.inventory_layout = BoxLayout(orientation='vertical', spacing=5)
        inventory_panel.add_widget(self.inventory_layout)
        root_layout.add_widget(equipment_panel)
        root_layout.add_widget(inventory_panel)
        back_button = Button(text="Zurück zur Stadt", size_hint=(None, None), size=(150, 50), pos=(10, 10))
        back_button.bind(on_press=self.back_to_city)
        self.add_widget(back_button)
        self.add_widget(root_layout)

    def on_enter(self):
        self.update_ui()

    def update_ui(self):
        self.update_equipment_ui()
        self.update_inventory_ui()

    def update_equipment_ui(self):
        self.equipment_layout.clear_widgets()
        app = App.get_running_app()
        for slot in EQUIPMENT_SLOTS:
            item_uid = app.player_data.equipment.get(slot)
            if item_uid:
                item_id = app.player_data.inventory.get(item_uid)
                item_name = ITEM_DATA[item_id]['name'] if item_id else "Leer"
                text = f"{slot.capitalize()}: {item_name}"
            else:
                text = f"{slot.capitalize()}: Leer"
            slot_button = Button(text=text, size_hint_y=None, height=40)
            slot_button.bind(on_press=lambda instance, s=slot, uid=item_uid: self.unequip_item(s, uid))
            self.equipment_layout.add_widget(slot_button)

    def update_inventory_ui(self):
        self.inventory_layout.clear_widgets()
        app = App.get_running_app()
        for unique_id, item_id in app.player_data.inventory.items():
            if unique_id not in app.player_data.equipment.values():
                item_name = ITEM_DATA[item_id]['name']
                item_button = Button(text=item_name, size_hint_y=None, height=40)
                item_button.bind(on_press=lambda instance, uid=unique_id, i_id=item_id: self.equip_item(uid, i_id))
                self.inventory_layout.add_widget(item_button)

    def equip_item(self, unique_id, item_id):
        app = App.get_running_app()
        item_type = ITEM_DATA[item_id]['type']
        target_slot = None
        if item_type in EQUIPMENT_SLOTS:
            if not app.player_data.equipment.get(item_type):
                target_slot = item_type
        elif item_type == 'rune':
            if not app.player_data.equipment.get('rune_1'):
                target_slot = 'rune_1'
            elif not app.player_data.equipment.get('rune_2'):
                target_slot = 'rune_2'
        if target_slot:
            app.player_data.equipment[target_slot] = unique_id
            app.player_data.save_data()
            self.update_ui()
            if hasattr(app, 'calculate_stats'):
                app.calculate_stats()
        else:
            print(f"Kein freier Slot für Item-Typ '{item_type}'")

    def unequip_item(self, slot, unique_id):
        if not unique_id: return
        app = App.get_running_app()
        if slot in app.player_data.equipment:
            del app.player_data.equipment[slot]
            app.player_data.save_data()
            self.update_ui()
            if hasattr(app, 'calculate_stats'):
                app.calculate_stats()

    def back_to_city(self, instance):
        App.get_running_app().screen_manager.current = 'city'