import kivy
kivy.require('2.3.0') # Ensure compatibility

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from game.screens import GameScreen, CardSelectionScreen

class IdleHordeSlayerApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        game_screen = GameScreen(name='game')
        self.screen_manager.add_widget(game_screen)

        card_selection_screen = CardSelectionScreen(name='card_selection')
        self.screen_manager.add_widget(card_selection_screen)

        # Die Referenz auf das GameWidget speichern, um darauf zugreifen zu können
        self.game_widget = game_screen.game_widget

        # Initialisierung der Boni
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
        # Basiswerte
        base_attack_damage = 10
        base_hero_speed = 100
        base_attack_speed = 0.5  # Sekunden pro Schuss

        # Berechnung der finalen Werte
        self.attack_damage = base_attack_damage * (1 + self.temp_damage_percent)
        self.hero_speed = base_hero_speed * (1 + self.temp_speed_percent)
        self.attack_cooldown = base_attack_speed / (1 + self.temp_attack_speed_percent)

        # Aktualisiert die Werte im Spiel
        if hasattr(self, 'game_widget'):
            self.game_widget.update_hero_stats(
                damage=self.attack_damage,
                speed=self.hero_speed,
                attack_cooldown=self.attack_cooldown
            )

if __name__ == '__main__':
    IdleHordeSlayerApp().run()