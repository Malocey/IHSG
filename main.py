import kivy
kivy.require('2.3.0') # Ensure compatibility

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from game.screens import GameScreen, CardSelectionScreen, SkillTreeScreen
from game.player_data import PlayerData
from game.skill_tree_data import SKILL_TREE_DATA

class IdleHordeSlayerApp(App):
    def build(self):
        self.player_data = PlayerData()
        self.screen_manager = ScreenManager()

        game_screen = GameScreen(name='game')
        self.screen_manager.add_widget(game_screen)

        card_selection_screen = CardSelectionScreen(name='card_selection')
        self.screen_manager.add_widget(card_selection_screen)

        skill_tree_screen = SkillTreeScreen(name='skill_tree')
        self.screen_manager.add_widget(skill_tree_screen)

        self.game_widget = game_screen.game_widget

        # Initialisierung der temporären Boni
        self.temp_damage_percent = 0
        self.temp_attack_speed_percent = 0
        self.temp_speed_percent = 0

        self.calculate_stats()
        return self.screen_manager

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

    def calculate_stats(self):
        """
        Berechnet die finalen Spielerstatistiken basierend auf permanenten und temporären Boni.
        """
        # Permanente Boni aus dem Skill-Tree berechnen
        perm_strength = 0
        perm_dexterity = 0
        perm_attack_speed_percent = 0

        for node_id in self.player_data.unlocked_nodes:
            node = SKILL_TREE_DATA.get(node_id)
            if not node:
                continue

            if node['type'] == 'strength':
                perm_strength += node['value']
            elif node['type'] == 'dexterity':
                perm_dexterity += node['value']
            elif node['type'] == 'notable':
                for bonus in node.get('bonuses', []):
                    if bonus['type'] == 'attack_speed_percent':
                        perm_attack_speed_percent += bonus['value']
                    elif bonus['type'] == 'dexterity':
                        perm_dexterity += bonus['value']

        # Basiswerte
        base_attack_damage = 10
        base_hero_speed = 100
        base_attack_speed = 0.5

        # Berechnung der finalen Werte
        self.attack_damage = (base_attack_damage + perm_strength) * (1 + self.temp_damage_percent)
        self.hero_speed = (base_hero_speed + perm_dexterity) * (1 + self.temp_speed_percent)
        self.attack_cooldown = base_attack_speed / (1 + perm_attack_speed_percent + self.temp_attack_speed_percent)

        # Aktualisiert die Werte im Spiel
        if hasattr(self, 'game_widget'):
            self.game_widget.update_hero_stats(
                damage=self.attack_damage,
                speed=self.hero_speed,
                attack_cooldown=self.attack_cooldown
            )

if __name__ == '__main__':
    IdleHordeSlayerApp().run()