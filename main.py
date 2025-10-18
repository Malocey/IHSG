import kivy
kivy.require('2.3.0') # Ensure compatibility

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from game.screens import GameScreen, CardSelectionScreen, SkillTreeScreen, CityScreen, ShopScreen
from game.player_data import PlayerData
from game.skill_tree_data import SKILL_TREE_DATA

class IdleHordeSlayerApp(App):
    _instance = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        IdleHordeSlayerApp._instance = self

    def build(self):
        self.player_data = PlayerData()
        self.screen_manager = ScreenManager()

        game_screen = GameScreen(name='game')
        self.screen_manager.add_widget(game_screen)

        card_selection_screen = CardSelectionScreen(name='card_selection')
        self.screen_manager.add_widget(card_selection_screen)

        skill_tree_screen = SkillTreeScreen(name='skill_tree')
        self.screen_manager.add_widget(skill_tree_screen)

        city_screen = CityScreen(name='city')
        self.screen_manager.add_widget(city_screen)

        shop_screen = ShopScreen(name='shop')
        self.screen_manager.add_widget(shop_screen)

        self.game_widget = game_screen.game_widget

        # Initialisierung der temporären Boni
        self.temp_damage_percent = 0
        self.temp_attack_speed_percent = 0
        self.temp_speed_percent = 0

        self.calculate_stats()
        Window.bind(on_key_down=self.on_key_down)
        return self.screen_manager

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40: # Enter
            Window.screenshot(name='verification.png')

    @staticmethod
    def get_instance(self):
        return IdleHordeSlayerApp._instance

    def apply_upgrade(self, card_data):
        """
        Wendet ein ausgewähltes Upgrade an und berechnet die Stats neu.
        """
        upgrade_type = card_data['type']
        value = card_data['value']

        if upgrade_type == 'damage_percent':
            self.temp_damage_percent += value
        elif upgrade_type == 'attack_speed_percent':
            self.temp_attack_speed_percent += value
        elif upgrade_type == 'speed_percent':
            self.temp_speed_percent += value

        self.calculate_stats()

from game.config import SHOP_UPGRADES

# ... (rest of the file)

    def calculate_stats(self):
        """
        Berechnet die finalen Spielerstatistiken basierend auf permanenten Boni aus Skills und Shop.
        """
        # Permanente Boni aus dem Skill-Tree
        perm_strength = 0
        perm_dexterity = 0
        perm_attack_speed_percent = 0
        # ... (andere Boni aus dem Skill-Tree)

        for node_id in self.player_data.unlocked_nodes:
            node = SKILL_TREE_DATA.get(node_id)
            if not node:
                continue

            if node.get('bonus_type') == 'strength':
                perm_strength += node.get('value', 0)
            elif node.get('bonus_type') == 'dexterity':
                perm_dexterity += node.get('value', 0)

            if node.get('node_type') == 'notable':
                for bonus in node.get('bonuses', []):
                    if bonus['type'] == 'attack_speed_percent':
                        perm_attack_speed_percent += bonus['value']
                    # ... (weitere notable Boni)

        # Permanente Boni aus dem Shop
        self.gold_find_percent = 0
        self.xp_gain_percent = 0
        self.shop_price_percent = 0

        for upgrade_id, level in self.player_data.shop_upgrades.items():
            upgrade_data = SHOP_UPGRADES.get(upgrade_id)
            if not upgrade_data:
                continue

            bonus_value = upgrade_data['bonus_per_level'] * level
            if upgrade_data['bonus_type'] == 'gold_find_percent':
                self.gold_find_percent += bonus_value
            elif upgrade_data['bonus_type'] == 'xp_gain_percent':
                self.xp_gain_percent += bonus_value
            elif upgrade_data['bonus_type'] == 'shop_price_percent':
                self.shop_price_percent += bonus_value

        # Basiswerte
        base_attack_damage = 10
        base_hero_speed = 100
        base_attack_speed = 0.5

        # Berechnung der finalen Werte
        self.attack_damage = (base_attack_damage + perm_strength) * (1 + self.temp_damage_percent)
        self.hero_speed = (base_hero_speed + perm_dexterity) * (1 + self.temp_speed_percent)
        self.attack_cooldown = base_attack_speed / (1 + perm_attack_speed_percent + self.temp_attack_speed_percent)

        # Aktualisiert die Werte im Spiel (diese bleiben hier, da sie die In-Run-Stats beeinflussen)
        if hasattr(self, 'game_widget'):
            self.game_widget.update_hero_stats(
                damage=self.attack_damage,
                speed=self.hero_speed,
                attack_cooldown=self.attack_cooldown
            )

if __name__ == '__main__':
    IdleHordeSlayerApp().run()